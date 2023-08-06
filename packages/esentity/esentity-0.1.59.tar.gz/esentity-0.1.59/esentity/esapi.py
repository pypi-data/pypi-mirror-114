#coding: utf-8
from flask import request, url_for, jsonify, session
from flask import current_app as app
from flask_restful import Resource
from flask_login import current_user, login_required
from esentity.models import Page, Actor, Guest
from datetime import date, datetime
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed
from PIL import Image
from resizeimage import resizeimage
import hashlib
from slugify import slugify 
import os
from loguru import logger
from werkzeug.routing import BuildError

class ApiPing(Resource):
    def get(self):
        return {'ok': True, 'pong': True}

class ApiResourceGet(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceGet: {0}'.format(data))

        if data:
            objs, total = Page.get(_id=data['key'])
            if total == 1:
                obj = objs.pop()
                doc = obj.to_dict()
                doc['updatedon'] = datetime.utcnow()
                resp = {
                    'ok': True,
                    'resource': doc,
                }
                return resp
        else:
            resp = {
                'ok': True,
                'resource': {
                    'alias': Page.get_random_string(10).lower(),
                    'category': 'slot',
                    'is_active': True,
                    'is_searchable': True,
                    'publishedon': datetime.utcnow().date(),
                    'updatedon': datetime.utcnow(),
                    'order': 0,
                    'locale': 'en'
                },
            }
            return resp
        return {'ok': False}

def get_page_url(obj):
    url = None

    kw = {
        'alias': obj['alias']
    }
    if app.config.get('CORE_PREFIX'):
        kw['lang_code'] = obj['locale']

    if obj['category'] == 'slot':
        url = url_for('{0}slot'.format(app.config.get('CORE_PREFIX', '')), **kw)
    elif obj['category'] == 'provider':
        url = url_for('{0}casino'.format(app.config.get('CORE_PREFIX', '')), **kw)
    else:
        url = url_for('{0}path'.format(app.config.get('CORE_PREFIX', '')), **kw)

    return url

class ApiResourceSearch(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceSearch: {0}'.format(data))

        objs, total = Page.get(path=data['key'], locale=data.get('locale', 'en'))
        if total:
            obj = objs.pop()


            data = [{
                'key': obj._id, 
                'title': obj.title or obj.path, 
                'url': get_page_url(obj.to_dict())
            }]
            resp = {
                'ok': True,
                'found': data, 
                'resource_key': data[0],
            }
        else:
            resp = {
                'ok': True,
                'found': [], 
                'resource_key': None
            }
        return resp

def get_tags(item):
    _tags = []
    if item.category == 'provider':
        _tags.append({'title': 'Casino', 'class': 'casino'})
    elif item.category == 'slot':
        _tags.append({'title': 'Slot', 'class': 'slot'})
    elif item.category == 'collection':
        _tags.append({'title': 'Collection', 'class': 'collection'})

    if not item.is_active:
        _tags.append({'title': 'Not Active', 'class': 'is-disabled'})
    if not item.is_searchable:
        _tags.append({'title': 'Not Searchable', 'class': 'not-searchable'})
    if item.is_redirect:
        _tags.append({'title': 'Redirect', 'class': 'is-redirected'})

    _tags.append({'title': item.locale.upper(), 'class': 'locale'})

    return _tags

class ApiResourceSearchPage(Resource):
    # @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceSearchPage: {0}'.format(data))

        objs = [{
            'key': item._id, 
            'title': item.title or item.path, 
            'url': get_page_url(item.to_dict()),
            'tags': get_tags(item)
        } for item in Page.query(data['query'], True)]
        return {'ok': True, 'items': objs}

class ApiResourceGeo(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceGeo: {0}'.format(data))

        _c, _e, _v = Page.get_countries(data.get('w', ''), data.get('b', ''))
        if _v:
            _c = []

        return {'ok': True, 'countries': _c, 'errors': _e}

class ApiResourceUpload(Resource):
    @login_required
    def post(self):
        logger.info(u'Data ApiResourceUpload: {0}'.format(request.form))

        _e = None
        try:
            resp = {}
            file = request.files['file']
            basename = slugify(u'.'.join(file.filename.split('.')[:-1])).lower() + '.'

            rename = request.form['rename']
            if rename in ['entity']:
                basename = slugify(request.form['title'] or basename).lower() + '.'
            if rename in ['hash']:
                basename = hashlib.md5(file.read()).hexdigest() + '.'
                file.seek(0)
            
            filename = app.images.save(file, None, basename)
            resp['origin'] = app.images.url(filename)

            path = app.images.path(filename)
            image = Image.open(path) 
            image = image.convert('RGBA')            
            w, h = image.size

            _w = None
            _h = None

            preset = request.form['preset'].split('_')
            for item in preset:
                if 'w' in item:
                    _w = int(item.replace('w', ''))
                elif 'h' in item:
                    _h = int(item.replace('h', ''))

            if len(preset) > 1:
                tfname = '{0}.' + preset[0] + '.png'
                filename = '.'.join(filename.split('.')[:-1])

                if _w and _h:
                    if w > _w and h > _h: 
                        image = resizeimage.resize_cover(image, [_w, _h])
                else:
                    if w > _w:
                        image = resizeimage.resize_width(image, _w)

                png = app.images.path(tfname.format(filename))
                image.save(png, 'PNG')
                resp['png'] = app.images.url(tfname.format(filename))

                image.save("{0}.webp".format(png), 'WEBP')
                resp['webp'] = "{0}.webp".format(resp['png'])
            else:
                image.save("{0}.webp".format(path), 'WEBP')
                resp['webp'] = "{0}.webp".format(resp['origin'])

            resp['ok'] = True
            return resp
        except UploadNotAllowed:
            _e = 'Not allowed'
        return {'ok': False, 'error': _e}

class ApiResourceSave(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceSave: {0}'.format(data))

        _errors = dict()
        entity = data['entity']

        # to cerberus
        if not entity.get('alias'):
            if entity.get('title'):
                entity['alias'] = entity['title']
            else:
                _errors['alias'] = ['Mandatory field']

        if not _errors:
            if entity['category'] in ['slot', 'provider']:
                entity['alias'] = slugify(entity['alias'].strip()).lower()

            resource_key = data['key']

            try:
                path = get_page_url(entity)
            except BuildError:
                _errors['category'] = ['Endpoint not found']

            if not _errors:
                if app.config.get('CORE_PREFIX'):
                    path = path.replace('/{0}'.format(entity['locale']), '')

                _, total = Page.get(path=path, locale=entity['locale'])

                if total > 0 and (not resource_key or (resource_key and resource_key.get('key') != _.pop()._id)):
                    _errors['alias'] = ['Page already exist: {0}'.format(path)]
                else:
                    if not resource_key:
                        _id = Page.generate_id(path, entity['locale'])
                    else:
                        _id = resource_key.get('key')

                    entity['path'] = path
                    entity['suggest'] = entity.get('title', '')
                    entity['project'] = os.environ.get('PROJECT', 'app')

                    if entity['category'] in ['provider']:
                        _c, _e, _v = Page.get_countries(entity.get('geo_whitelist', ''), entity.get('geo_blacklist', ''))
                        logger.debug('GEO found: {0}'.format(len(_c)))
                        if not _v:
                            entity['geo'] = _c
                    else:
                        entity['geo'] = []

                    resp, obj = Page.put(_id, entity)
                    return {'ok': True}

        return {'ok': False, 'errors': _errors}

class ApiResourceHistory(Resource):
    @login_required
    def post(self):
        history, found = Page.get(_count=20, _sort=[{"updatedon": {"order": "desc"}}])
        objs = [{
            'key': item._id, 
            'title': item.title or item.path, 
            'url': get_page_url(item.to_dict()),
            'tags': get_tags(item)
        } for item in history]
        return {'ok': True, 'history': objs}

class ApiResourceAPISearch(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        logger.info(u'Data ApiResourceAPISearch: {0}'.format(data))
        return {'ok': True, 'items': ['berryburst', 'dr-fortuno']}

class ApiAuth(Resource):
    def get(self):
        doc = {
            'id': 'admin',
            'username': 'admin',
            'actor_is_active': True,
            'actor_is_admin': True,
            'ip': request.remote_addr,
            'ua': str(request.user_agent),
            'cid': '',
        }
        session['actor'] = doc
        return doc

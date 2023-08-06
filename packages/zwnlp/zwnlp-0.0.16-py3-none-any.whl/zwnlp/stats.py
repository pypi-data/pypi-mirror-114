import re
from pathlib import Path

from zwutils.fileutils import readfile, readjson
from zwutils.textutils import inner_trim
from zwdb.zwmongo import ZWMongo
from zwutils.dlso import upsert_config
from zwutils.geoutils import address2adcode

from zwutils.logger import logger
LOG = logger(__name__)
CODES = readjson('./data/codetree.json')

COLL_GOVRPT = 'govrpt'
COLL_GOVRPT_IDX = 'govrpt_idx'

class Stats(object):
    def __init__(self, pth, cfg=None, **kwargs):
        cfgdef = {
            'db': 'mongo://localhost:27017/gfman',
        }
        self.cfg = upsert_config({}, cfgdef, cfg, kwargs)
        self.pth = Path(pth)
        self.txt = readfile(pth)
        self.tagid_count = 0

        self.bad_report_filename = False
        self.adcode = None
        self.rptyear = None
        fn = self.pth.stem
        r = re.search('^(\d{4})年', fn)
        if not r:
            self.bad_report_filename = True
        else:
            year = r.group(1)
            fn = fn[5:]
            adcode = address2adcode(fn, CODES)
            if not adcode:
                self.bad_report_filename = True
            else:
                self.adcode = adcode
                self.rptyear = year

    def tags(self):
        dat = self.classify()
        for i,o in enumerate(dat):
            if len(o['children'])>0:
                for p in o['children']:
                    t = p['text']
                    p['tags'] = self.get_tags(t, p)
            else:
                t = o['text']
                o['tags'] = self.get_tags(t, o)
        return dat

    def classify(self):
        dat = []
        arr = re.split(r'\n[一二三四五六七八九十]{1,2}、(.+)\n', self.txt)
        arr = arr[1:]
        for i in range(0, len(arr)-1, 2):
            nme = inner_trim(arr[i])
            tit = nme
            txt = arr[i+1]
            tid = str(self.tagid_count)
            iid = self.get_idxid(nme)
            self.tagid_count += 1
            children = []

            _arr = re.split(r'（[一二三四五六七八九十]{1,2}）(.+?)。', txt)
            _arr = [o.strip() for o in _arr if o.strip()!= '']
            for j in range(0, len(_arr)-1, 2):
                _nme = inner_trim(_arr[j])
                _tit = _nme
                _txt = _arr[j+1]
                _tid = str(self.tagid_count)
                _iid = self.get_idxid('%s_%s'%(nme, _nme))
                self.tagid_count += 1
                children.append({
                    'title' : _tit,
                    'name'  : _nme,
                    'text'  : _txt,
                    'tag_id': _tid,
                    'idx_id': _iid,
                })

            o = {
                'title' : tit,
                'name'  : nme,
                'text'  : txt,
                'tag_id': tid,
                'idx_id': iid,
                'children': children,
            }
            dat.append(o)
        return dat

    def get_tags(self, txt, parent):
        sents = txt.split('。')
        sents = [s.strip() for s in sents if self.contains_digit(s) and s.strip()!='']
        num_words = ['为','达']
        cls_words = ['其中']
        cmp_words = ['比','较']
        pct_words = ['占']
        inc_words = ['增长','增加','减少','提高','下降']
        tags = []
        for i,s in enumerate(sents):
            s = re.sub(r'\s', '', s)
            arr = s.split('，')
            arr = [o for o in arr if self.contains_digit(o)]
            rootname = None

            for j,t in enumerate(arr):
                LOG.info('*'*50)
                LOG.info(t)
                cmp_base = ''
                cmp_type = ''
                t = re.sub(r'[1-9]\d{3}年', '', t)
                t = re.sub(r'[1-9]\d{3}-', '', t)
                a = re.split(r'([-+]?[0-9]*\.?[0-9]+)', t)
                if len(a)>=3 and '（' in a[2]:
                    a = a[:3]
                    idx = a[2].find('（')
                    a[2] = a[2][:idx]
                if len(a)==3:
                    nm = a[0]
                    val = a[1]
                    unt = a[2]
                    if any(nm.endswith(k) for k in num_words):
                        nm = nm[:-1]
                    if any(nm.startswith(k) for k in cmp_words):
                        nm = nm[1:]
                        for o in inc_words:
                            idx = nm.find(o)
                            if idx != -1:
                                cmp_base = nm[:idx]
                                cmp_type = nm[idx:]
                                break
                        nm = rootname if rootname else nm
                    if any(nm.startswith(k) for k in inc_words):
                        for o in inc_words:
                            idx = nm.find(o)
                            if j != -1:
                                cmp_base = nm[:idx]
                                cmp_type = nm[idx:]
                                break
                        nm = rootname if rootname else nm
                    if nm is None:
                        bbb = 0
                    if any(nm.startswith(k) for k in pct_words):
                        idx = nm.find(val)
                        cmp_base = nm[1:idx]
                        if cmp_base.endswith('的'):
                            cmp_base = cmp_base[:-1]
                        cmp_type = '占'
                        nm = rootname if rootname else nm
                    for o in cls_words:
                        nm = re.sub(o, '', nm)
                    
                    nm = nm[1:] if nm.startswith('：') else nm
                    nm = inner_trim(nm)
                    tid = str(self.tagid_count)
                    iid = '%s_%s_%s'%(parent['idx_id'], nm, unt)
                    self.tagid_count += 1
                    o = {
                        'title' : nm,
                        'name'  : nm,
                        'text'  : t,
                        'tag_id': tid,
                        'idx_id': iid,
                        'value' : val,
                        'unit'  : unt,
                        'cmp_type': cmp_type,
                        'cmp_base': cmp_base,
                    }
                    tags.append(o)
                    if j == 0:
                        rootname = nm
        return tags

    def get_idxid(self, key):
        # TODO 指标体系映射
        return key
        # cfg =self.cfg
        # with ZWMongo(cfg.db) as db:
        #     conds = {
        #         'adcode': self.adcode,
        #         'idxkey': key
        #     }
        #     exists = db.exists(COLL_GOVRPT_IDX, conds=conds)


    def rpttext(self, dat):
        rtn = []
        for i,o in enumerate(dat):
            txt = '<div tag_id="%s">%s</div>'%(o['tag_id'], o['text'])
            t = self.get_tagstext(txt, o)
            rtn.append(t)
        return '<br>'.join(rtn)

    def get_tagstext(self, txt, o):
        tags = o['tags'] if 'tags' in o else []
        for j,p in enumerate(tags):
            txt = txt.replace(p['text'], '<div tag_id="%s">%s</div>'%(p['tag_id'], p['text']))
        if 'children' in o and len(o['children'])>0:
            for p in o['children']:
                txt = txt.replace(p['text'], '<div tag_id="%s">%s</div>'%(p['tag_id'], p['text']))
                txt = self.get_tagstext(txt, p)
        return txt
    
    def contains_digit(self, txt):
        for c in txt:
            if c.isdigit():
                return True
        return False



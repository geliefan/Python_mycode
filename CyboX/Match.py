#-*- coding:utf-8 -*-
'''
Created on 2015/01/29

@author: http://d.hatena.ne.jp/shomah4a/20100215/1266246945
'''

import itertools


class MatchProxy(object):

    def __init__(self, obj, name):

        self.name = name
        self.obj = obj

    def setvalue(self, value):

        self.obj._matchResult[self.name] = value



def check(typ, v, g):

    if isinstance(v, typ) and isinstance(g, typ):
        return True


class Match(object):
    #パターンマッチ
    def __init__(self, target):

        self.target = target

        self._matchResult = {}


    def __getattr__(self, name):
        '''
        値を取得
        '''

        try:
            return super(Match, self).__getattr__(name)
        except AttributeError:
            pass

        if name in self._matchResult:
            return self._matchResult[name]

        return MatchProxy(self, name)


    def when(self, guard):
        '''
        パターンマッチング
        '''

        self._matchResult = {}

        return self.matchOne(self.target, guard)


    def matchOne(self, val, guard):
        '''
        値に対するマッチ
        '''

        if isinstance(guard, MatchProxy):
            guard.setvalue(val)
            return True

        if self.matchIterable(val, guard):
            return True

        if self.matchDict(val, guard):
            return True

        if self.matchObject(val, guard):
            return True
        
        if self.matchType(type(val), val, guard):
            return True

        # 最終的には等価であるかどうかを調べる
        return val == guard


    def matchType(self, typ, v, g):
        '''
        とりあえず値チェック
        '''

        if not check(typ, v, g):
            return False

        return v == g


    def matchIterable(self, val, guard):
        '''
        list, tuple とマッチ
        '''

        def check(typ):
            if isinstance(val, typ) and isinstance(guard, typ):
                return True

        if not (check(list) or check(tuple)):
            return False
            
        if len(val) == len(guard):
            for v, g in itertools.izip(val, guard):
                if not self.matchOne(v, g):
                    return False
        else:
            return False

        return True


    def matchDict(self, val, guard):
        '''
        辞書とマッチ
        全値をカバーする必要はない
        '''

        if not (isinstance(val, dict) and isinstance(guard, dict)):
            return False


        for k, v in guard.iteritems():
            if not (k in val and self.matchOne(val[k], v)):
                return False

        return True


    def matchObject(self, val, guard):
        '''
        手抜きで辞書とマッチさせる
        '''

        if not isinstance(guard, dict):
            return False

        for k, v in guard.iteritems():
            if not (hasattr(val, k) and self.matchOne(getattr(val, k), v)):
                return False

        return True



def test():

    m = Match(10)

    m.when(m.val)
    
    print m.val
    
    assert m.when(10)

    assert m.when(m.val) and m.val == 10

    
    m = Match([1,2,3])

    assert m.when([1,2,3])
    
    assert m.when(m.val) and m.val == [1,2,3]

    assert m.when([1, m.el1, m.el2]) and m.el1 == 2 and m.el2 == 3

    d = dict(x=10, y=20.0, z="aaaa")
    m = Match(d)

    assert m.when(d)

    assert m.when(dict(x=m.aa, y=m.bb, z="aaaa")) and m.aa == 10 and m.bb == 20.0


    class test:
        pass

    t = test()
    t.x = 10
    t.y = [1,2,3]
    t.z = (1,2,3)
    t.a = u"bbbb"

    m = Match(t)

    assert m.when(dict(x=m.x, y=m.y, z=m.z)) and m.x == t.x and m.y == t.y and m.z == t.z

    comp = [1,dict(x=10,y=20), t, (1,2,3)]
    m = Match(comp)

    assert m.when([1, dict(y=m.y), dict(a=m.a), (1,m.val,3)]) and \
        m.y == 20 and m.a == u"bbbb" and m.val == 2
    


if __name__ == '__main__':
    test()
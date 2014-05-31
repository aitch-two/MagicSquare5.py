#! /usr/bin/env python
# coding: UTF-8
# Python2.7で魔方陣5x5全解列挙
from __future__ import print_function

class MagicSquare5 :
    """ 魔方陣を全解列挙するイテレータクラス """

    def __init__(self):
        """ コンストラクタでは何もしない """
        pass

    def __iter__(self):
        """ 処理の本体は genrow() ジェネレータ """
        return self.genrow(set(), self.sqtab, self.sqtab, self.sqtab)

    def mk_sqtab() : # NOT a method
        """ 1～25から5つ選んで合計が65になる組み合わせのsetを返す（1394通り） """
        n = [0, 0, 0, 0, 0]
        nb = [0, 0, 0, 0, 0]
        sqtab = set()
        for n[0] in range(1, 1 + 25) :
            nb[0] = 1 << n[0]
            for n[1] in range(1, n[0]) :
                nb[1] = 1 << n[1]
                for n[2] in range(1, n[1]) :
                    nb[2] = 1 << n[2]
                    for n[3] in range(1, n[2]) :
                        nb[3] = 1 << n[3]
                        for n[4] in range(1, n[3]) :
                            nb[4] = 1 << n[4]
                            if 65 == sum(n) :
                                sqtab.add(sum(nb))
        return sqtab

    def mk_bittab() : # NOT a method
        """ 各ビットをキーとして、出力する文字を値とするdictionaryを返す """
        bittab = {}
        for n in range(1, 1 + 25) :
            bittab[1 << n] = "-123456789abcdefghijklmnop"[n]
        return bittab

    def mk_pattern(t) : # NOT a method
        """ 一つの解から、置換で別の解を生成するパターンを作る """
        pp = []
        for j in t :
            for i in t :
                pp.append(i + 5 * j)
        return pp

    pattern04 = mk_pattern((4, 1, 2, 3, 0))
    pattern0134 = mk_pattern((1, 0, 2, 4, 3))
    pattern13 = mk_pattern((3, 0, 2, 4, 1))
    bitall = ~(~0 << 25) << 1
    sqtab = mk_sqtab()
    bittab = mk_bittab()

    def genrow(self, r, rr, cc, dd) :
        """ 再帰的に行の候補から行を選ぶ。すでに5行選ばれている場合は、列を選択する処理を呼ぶ。
         r: すでに選ばれた行の集合, rr: 行の候補の集合, cc: 列の候補の集合, dd: 対角線の候補の集合 """
        if len(r) < 5 :
            # row
            for curr in rr :
                nextrr = set()
                checkor = curr
                for n in r :
                    checkor |= n
                for n in rr :
                    if 0 == (n & curr) and n < curr :
                        nextrr.add(n)
                        checkor |= n
                if checkor != self.bitall :
                    continue
                nextcc = set()
                checkor = 0
                if len(r) == 0 :
                    for n in cc :
                        if (n & curr) in self.bittab and n < curr :
                            nextcc.add(n)
                            checkor |= n
                else :
                    for n in cc :
                        if (n & curr) in self.bittab :
                            nextcc.add(n)
                            checkor |= n
                if checkor != self.bitall :
                    continue
                nextdd = set()
                for n in dd :
                    if (n & curr) in self.bittab :
                        nextdd.add(n)
                if len(nextdd) < 2 :
                    continue
                for ret in self.genrow(r | set([curr]), nextrr, nextcc, nextdd) :
                    yield ret 
        else :
            for ret in self.gencolumn(r, set(), cc, dd) :
                yield ret 

    def gencolumn(self, r, c, cc, dd) :
        """ 再帰的に列の候補から列を選ぶ。すでに5列選ばれている場合は、対角線を選択する処理を呼ぶ。
        r: 選ばれた行の集合, c: すでに選ばれた列の集合, cc: 列の候補の集合, dd: 対角線の候補の集合 """
        if len(c) < 5 :
            # column
            for curc in cc :
                nextcc = set()
                checkor = curc
                for n in c :
                    checkor |= n
                for n in cc :
                    if 0 == (n & curc) and n < curc :
                        nextcc.add(n)
                        checkor |= n
                if checkor != self.bitall :
                    continue
                nextdd = set()
                for n in dd :
                    if (n & curc) in self.bittab :
                        nextdd.add(n)
                if len(nextdd) < 2 :
                    continue
                for ret in self.gencolumn(r, c | set([curc]), nextcc, nextdd) :
                    yield ret 
        else :
            for ret in self.gendiagonal(r, c, set(), dd) :
                yield ret 

    def gendiagonal(self, r, c, d, dd) :
        """ 再帰的に対角線の候補から対角線を選ぶ。すでに2つ選ばれている場合は、魔方陣文字列を生成する処理を呼ぶ。
        r: 選ばれた行の集合, c: 選ばれた列の集合, d: すでに選ばれた対角線の集合, dd: 対角線の候補の集合 """
        if len(d) < 2 :
            # diagonal
            for curd in dd :
                nextdd = set()
                for n in dd :
                    if (n & curd) in self.bittab and n < curd :
                        nextdd.add(n)
                if 1 + len(d) + len(nextdd) < 2 :
                    continue
                for ret in self.gendiagonal(r, c, d | set([curd]), nextdd) :
                    yield ret
        else :
            for ret in self.gensquare(r, c, d) :
                yield ret

    def subst(self, s, pattern) :
        """ 与えられたパターンにしたがって文字列の文字を入れ替える """
        t = ""
        for p in pattern :
            t += s[p]
        return t

    def gensquare(self, r, c, d) :
        """ 魔方陣文字列を生成する。魔方陣とならない組み合わせの場合はreturnする。
        r: 選ばれた行の集合, c: 選ばれた列の集合, d: 選ばれた対角線の集合 """
        listd = list(d)
        ra = {}
        for n in r :
            ra[n & listd[0]] = n
        cb = {}
        for n in c :
            cb[n & listd[1]] = n
        listr = [0, 0, 0, 0, 0]
        listc = [0, 0, 0, 0, 0]
        for rx in r :
            if rx & listd[0] & listd[1] :
                listr[2] = rx
                listc[2] = cb[rx & listd[1]]
            else :
                cx = cb[rx & listd[1]]
                ry = ra[cx & listd[0]]
                cy = cb[ry & listd[1]]
                rz = ra[cy & listd[0]]
                if rx != rz :
                    # 魔方陣にならない組み合わせ
                    return
                elif rx not in listr :
                    if listr[0] == 0 :
                        listr[0] = rx
                        listr[4] = ry
                        listc[0] = cx
                        listc[4] = cy
                    else :
                        listr[1] = rx
                        listr[3] = ry
                        listc[1] = cx
                        listc[3] = cy
            if 0 not in listr :
                break
        s = ""
        for j in range(5) :
            for i in range(5) :
                s += self.bittab[listr[j] & listc[i]]
        # 一つの組み合わせから4つの魔方陣が生成できる
        yield s
        yield self.subst(s, self.pattern04)
        yield self.subst(s, self.pattern0134)
        yield self.subst(s, self.pattern13)

if __name__ == '__main__':
    import sys
    import time
    start = time.clock()

    n = 0
    for s in MagicSquare5() :
        n += 1
        print(s)
        if 0 == n % 100000 :
            t = time.clock() - start
            print(n, "/", t, "=", n / t, s, file = sys.stderr)

    t = time.clock() - start
    print(n, "/", t, "=", n / t, "done.", file = sys.stderr)
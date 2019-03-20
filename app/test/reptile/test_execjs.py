# -*- coding: utf-8 -*-
import execjs


def test():
    ret = execjs.eval("'red yellow blue'.split(' ')")
    print(ret)
    # execjs.eval("console.log(123)")


if __name__ == '__main__':
    test()

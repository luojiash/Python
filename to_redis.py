#coding: utf-8

import re, urllib, urllib2, json
import mytool, zhihu

m = {
    r'EhCacheUtil.get([^;]*,\s*)([^;]*)\)': r'RedisUtil.getJedisX().hGetObject\1Integer.toString(\2))',
    r'EhCacheUtil.save([^;]*,\s*)([^;]*),': r'RedisUtil.getJedisX().hSetObject\1Integer.toString(\2),',
    r'EhCacheUtil.remove([^;]*,\s*)([^;]*)\)': r'RedisUtil.getJedisX().hDelete\1Integer.toString(\2))',
    r'import com.gongfutrip.util.EhCacheUtil;': r'import com.gongfutrip.redis.RedisUtil;'
}
def ehcache_to_redis(f_path):
    f = open(f_path, 'r+')
    f_content = f.read()
    for k in m:
        f_content = re.sub(k, m[k], f_content)
    f.seek(0)
    f.write(f_content)#err: 覆盖式写入，文件内容减少时，最后一些内容没有被覆盖
    f.close()

if __name__ == '__main__':
    mytool.filefunc = ehcache_to_redis
    #mytool.oswalk(r'C:\programs\workspace\gongfu-platform\platform-web')

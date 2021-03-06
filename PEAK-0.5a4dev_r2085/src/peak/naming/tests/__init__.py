"""Naming system tests

 The following schemes are not currently tested:

    * 'nis', 'unix', 'unix.dg', 'logging.logger', 'zconfig.schema', and
      'shellcmd' -- these do not have parsed bodies

    * 'pgsql', 'psycopg', 'mockdb' -- these all are based on 'GenericSQL_URL',
      which is tested by the 'sybase' test case.

    * 'sqlite' -- it's a 'file:' URL in disguise

    * 'nulllockfile', 'shlockfile', 'flockfile', 'winflockfile' -- these are
      all based on 'lockfileURL', which is tested by the 'lockfile' test case.
"""

from unittest import TestCase, makeSuite, TestSuite
from peak.api import *
from peak.tests import testRoot
from peak.naming.factories import openable
from urllib import quote




















validNames = {

    'smtp://spaz@foo':
        Items(host='foo', port=25),

    'smtp://foo.bar:8025':
        Items(host='foo.bar', port=8025),

    'ldap://cn=root:somePw@localhost:9912/cn=monitor':
        Items(
            host='localhost', port=9912, basedn=(('cn=monitor',),),
            extensions={'bindname':(1,'cn=root'), 'x-bindpw':(1,'somePw')},
            critical=('bindname','x-bindpw'),
        ),

    'ldap://localhost/cn=Bar,ou=Foo,o=eby-sarna.com/x':
        Items(
            host='localhost', port=389,
            basedn=(('o=eby-sarna.com','ou=Foo','cn=Bar'),'x'),
        ),

    'ldap://localhost/cn=Bar,ou=Foo,o=eby-sarna.com%2Fx':
        Items(
            host='localhost', port=389,
            basedn=(('o=eby-sarna.com/x','ou=Foo','cn=Bar'),),
        ),

    'ldap:///cn="A \\"quoted\\", and obscure thing",ou=Foo\\,Bar':
        Items(
            basedn=(('ou=Foo\\,Bar','cn="A \\"quoted\\", and obscure thing"',),)
        ),

    'uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8':
        Items(uuid='6ba7b810-9dad-11d1-80b4-00c04fd430c8', quals=()),

    'uuid:00000000-0000-0000-0000-000000000000;ext1=1;ext2=2':
        Items(uuid='00000000-0000-0000-0000-000000000000',
              quals=(('ext1','1'), ('ext2','2'))
        ),


    'sybase:foo:bar@baz/spam':
        Items(server='baz', db='spam', user='foo', passwd='bar'),
    'sybase://user:p%40ss@server':
        Items(server='server', db=None, user='user', passwd='p@ss'),

    'gadfly://drinkers@c:\\temp': Items(db='drinkers', dir=r'c:\temp'),

    'import:bada.bing':
        Items(body='bada.bing'),

    'lockfile:/c:\\spam.lock':
        Items(path=('','c:\\spam.lock',)),

    'config:environ.TMP/':
        Items(scheme='config', body=(('environ','TMP'),'') ),

    'logfile:/foo/bar?level=WARNING':
        Items(scheme='logfile', path=('','foo','bar'), level='WARNING'),

    'win32.dde:foo::bar;file=c:\\baz;retries=24;sleep=42':
        Items(scheme='win32.dde', service='foo', topic='bar', file='c:\\baz',
              retries=24, sleep=42),

    'file://localhost/D|/autoexec.old':
        Items(scheme='file', host='localhost',
                path=('','D|','autoexec.old'), query=None,),

    'pkgfile:peak/peak.ini': Items(scheme='pkgfile',module='peak',
        path=('peak.ini',)),
    'cxoracle:u:p@s': Items(user='u',passwd='p',server='s'),
    'dcoracle2://usr@srv/': Items(user='usr',server='srv'),
    'tcp://localhost:http': Items(host='localhost',port='http'),
    'udp://127.0.0.1:80': Items(host='127.0.0.1',port='80'),  # ugh
    'fd.socket:0/inet/stream/ip': Items(fileno=0, protocol=0),
    'fd.socket:stderr': Items(fileno=2),
    'fd.socket:27/inet/dgram': Items(fileno=27),
    'fd.socket:27//dgram': Items(fileno=27),
    'fd.file:stderr': Items(fileno=2),
    'ref:some.thing@some|URL||secondURL':
        Items(factoryName='some.thing',addresses=('some|URL','secondURL')),

    'icb://nik:u@localhost/aGroup':
        Items(nick='nik',user='u',passwd=None,server='localhost',
            group='aGroup'),

    'icb://n:u:p@localhost':
        Items(nick='n',user='u',passwd='p',server='localhost',
            group=None),

    'http://u:pw@serv:8080/some/thing?query=whatever#pos':
        Items(user='u',passwd='pw',host='serv',port=8080,fragment='pos',
            query='query=whatever',path=('some','thing')
        ),

    'ftp://serv/some/thing#pos':
        Items(user=None,passwd=None,host='serv',port=None,fragment='pos',
            path=('some','thing')
        ),

    'https://u@serv/some%2Fslashed/thing?query=whatever&who':
        Items(user='u',passwd=None,host='serv',port=None,fragment=None,
            query='query=whatever&who',path=('some/slashed','thing')
        ),

    'data:text/plain,foo%20bar':
        Items(content_type="text/plain",data="foo bar"),

    'data:text/plain;x=y,foo%20bar':
        Items(content_type="text/plain",data="foo bar",
            parameters=('x=y',)
        ),

    'data:text/plain;x=y;base64,foo%20bar':
        Items(content_type="text/plain",data="foo bar",
            parameters=('x=y','base64')
        ),
}





def parse(url,base=None):
    return naming.parseURL(testRoot(),url,base)


canonical = {
    'ldap://cn=root:somePw@localhost:9912/cn=monitor':
    'ldap://localhost:9912/cn=monitor????!bindname=cn=root,!x-bindpw=somePw',
    'sybase://user:p%40ss@server': 'sybase:user:p%40ss@server',
    'gadfly://drinkers@c:\\temp': 'gadfly:drinkers@c:\\temp',
    'dcoracle2://usr@srv/': 'dcoracle2:usr@srv',
    'fd.socket:0/inet/stream/ip': 'fd.socket:stdin',
    'fd.socket:27/inet/dgram': 'fd.socket:27//dgram',

}


class TestFactory(binding.Singleton):

    protocols.advise(classProvides=[naming.IObjectFactory])

    def getObjectInstance(self, context, refInfo, name, attrs=None):
        return list(refInfo.addresses)


class ReferenceTests(TestCase):

    def testRefRestore(self):
        ref = naming.Reference('peak.naming.tests.TestFactory',['x','y','z'])
        self.assertEqual( ref.restore(testRoot(),''), ['x','y','z'] )

    def testRefLookup(self):
        url ='ref:peak.naming.tests.TestFactory@xyz'
        self.assertEqual( testRoot().lookupComponent(url), ['xyz'] )








class NameParseTest(TestCase):

    def testValidAndCanonical(self):

        for name in validNames:

            stdform = canonical.get(name,name)
            parsed  = parse(name)

            # string formats should compare equal
            self.assertEqual([name,stdform], [name,str(parsed)])

            # parsed forms should also compare equal
            self.assertEqual(parse(stdform),parsed)


    def testData(self):
        for name,values in validNames.items():
            obj = parse(name)
            for (k,v) in values:
                self.assertEqual([k,getattr(obj,k)], [k,v])

        # Ensure that canonical forms have the same values
        for name,stdform in canonical.items():
            obj = parse(stdform)  # ensure
            for (k,v) in validNames[name]:
                self.assertEqual([k,getattr(obj,k)], [k,v])

    def testNotFound(self):
        try:
            testRoot().lookupComponent('noSuchNameShouldBeFound')
        except exceptions.NameNotFound:
            pass
        else:
            raise AssertionError("Should've raised NameNotFound")






relatives = [
    ('file:/x/y/z', 'a', 'file:/x/y/a'),
    ('https://foo.bar/baz/spam', '../wiz', 'https://foo.bar/wiz'),
    ('https://foo.bar/baz/spam', '/wiz', 'https://foo.bar/wiz'),
    ('https://foo.bar/baz/spam', '//wiz/', 'https://wiz/'),
    ('pkgfile:foo.bar/spam', 'foo', 'pkgfile:foo.bar/foo'),
    ('pkgfile:foo.bar/spam/', 'foo', 'pkgfile:foo.bar/spam/foo'),   # XXX
    ('pkgfile:foo.bar/spam', 'file:/x/y/z', 'file:/x/y/z'),
]

relative_errors = [
    ('pkgfile:foo.bar/spam', '../foo', ),
    ('pkgfile:foo.bar/spam', '/foo', ),
    ('pkgfile:foo.bar/spam', '//foo', ),
]

class OpenableTests(TestCase):

    def testDataURL(self):
        from peak.naming.factories.openable import ConstantStream
        factory = ConstantStream('abcdefg')
        assert factory.open('b').read() == "abcdefg"

        factory = testRoot().lookupComponent('data:,abcdefg')
        assert factory.open('b').read() == "abcdefg"

        factory = testRoot().lookupComponent('data:;base64,'
            +quote('abcdefg'.encode('base64')))
        assert factory.open('b').read() == "abcdefg"

    def testRelativeURLs(self):
        for base,rel,url in relatives:
            self.assertEqual(str(parse(rel,base)), url)

    def testRelativeErrors(self):
        for base, rel in relative_errors:
            self.assertRaises(exceptions.InvalidName,
                parse, rel, base)



from peak.naming.api import CompoundName as lname, CompositeName as gname
from peak.storage.LDAP import ldapURL as LU, distinguishedName as dN

additions = [
    ( dN('ou=foo,o=eby-sarna.com'), dN('cn=bar'),
        dN('cn=bar,ou=foo,o=eby-sarna.com')
    ),
    ( LU('ldap','///ou=foo,o=eby-sarna.com'), dN('cn=bar'),
        LU('ldap','///cn=bar,ou=foo,o=eby-sarna.com')
    ),
    ( LU('ldap','///ou=foo,o=eby-sarna.com'), gname([dN('cn=bar')]),
        LU('ldap','///cn=bar,ou=foo,o=eby-sarna.com')
    ),
    ( lname(['x','y']), lname(['z']), lname(['x','y','z']) ),
    ( '', lname(['foo']), lname(['foo']) ),
    ( gname(['a','b','']), lname(['x']), gname(['a','b',lname(['x'])]) ),
    ( gname(['a','b','']), gname(['','c']), gname(['a','b','','c']) ),
]

class NameAdditionTest(TestCase):
    def testAdds(self):
        for n1,n2,res in additions:
            assert n1+n2==res, (n1,n2,n1+n2,res)


TestClasses = (
    NameParseTest, NameAdditionTest, ReferenceTests, OpenableTests
)


def test_suite():
    s = []
    for t in TestClasses:
        s.append(makeSuite(t,'test'))

    return TestSuite(s)






# pylint: skip-file
import os
import tempfile
import unittest

from .. import etc


class EditableTextConfigurationTestCase(unittest.TestCase):

    def test_render_with_variable(self):
        value = etc.render('${foo}', foo='bar')
        self.assertEqual(value, 'bar')

    def test_render_environment_variable(self):
        os.environ['FOO'] = 'bar'
        value = etc.render('${env.FOO}')
        self.assertEqual(value, 'bar')

    def test_load_simple(self):
        with tempfile.NamedTemporaryFile('w+') as f:
            f.write(
                'foo:\n'
                '  bar: 1'
            )
            f.seek(0)
            data = etc.load(f.name)
        self.assertIn('foo', data)
        self.assertIn('bar', data['foo'])
        self.assertEqual(data['foo']['bar'], 1)

    def test_load_simple(self):
        os.environ['FOO'] = 'bar'
        with tempfile.NamedTemporaryFile('w+') as f:
            f.write(
                'foo: ${env.FOO}\n'
            )
            f.seek(0)
            data = etc.load(f.name)
        self.assertIn('foo', data)
        self.assertEqual(data['foo'], 'bar')

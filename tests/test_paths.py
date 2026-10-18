import contextlib
import io
import os
from pathlib import Path
import runpy
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from urllib.parse import unquote

from web.app import app


root = Path(__file__).resolve().parents[1]


class PathTests(unittest.TestCase):
    def test_web_screens_and_calculation(self):
        client = app.test_client()
        for cwd in (root, root.parent):
            with contextlib.chdir(cwd):
                for route in ('/', '/posture', '/intensity', '/diet'):
                    with self.subTest(cwd=cwd, route=route):
                        self.assertEqual(client.get(route).status_code, 200)
                response = client.post('/calculate', data={
                    'gender': 'male', 'weight': '70', 'height': '175', 'smm': '30',
                })
                self.assertEqual(response.status_code, 200)
                self.assertIn('52.50 kg', response.get_data(as_text=True))

    def test_ai_subprocess_paths_and_results(self):
        client = app.test_client()
        cases = (
            ('/process', {'image_url': 'https://example.com/squat.jpg'},
             'posture_analysis.py', ['https://example.com/squat.jpg']),
            ('/process_2', {'muscle_mass': '30', 'foods': 'eggs'},
             'diet_advice.py', ['30', 'eggs']),
        )
        for cwd in (root, root.parent):
            with contextlib.chdir(cwd):
                for route, data, script, args in cases:
                    for code, stdout, stderr, expected in (
                        (0, 'mock success\n', '', 'mock success'),
                        (1, '', 'mock failure\n', 'Error: mock failure'),
                    ):
                        with self.subTest(cwd=cwd, route=route, code=code):
                            with patch('web.app.subprocess.run', return_value=SimpleNamespace(
                                returncode=code, stdout=stdout, stderr=stderr,
                            )) as run:
                                response = client.post(route, data=data)
                            self.assertEqual(response.status_code, 200)
                            self.assertIn(expected, response.get_data(as_text=True))
                            run.assert_called_once_with(
                                [sys.executable, str(root/'web'/script), *args],
                                capture_output=True, text=True,
                            )
                            self.assertTrue((root/'web'/script).is_file())
                    with patch('web.app.subprocess.run', side_effect=OSError('mock error')):
                        response = client.post(route, data=data)
                    self.assertIn('Exception occurred: mock error', response.get_data(as_text=True))

    def test_gpt_asset_paths_without_api(self):
        scripts = [root/'web/posture_analysis.py', *sorted((root/'experiments/gpt').glob('*.py'))]
        response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='mock response'))])
        for cwd in (root, root.parent):
            with contextlib.chdir(cwd):
                for ref in ('main', 'codex/structure-cleanup'):
                    for script in scripts:
                        with self.subTest(cwd=cwd, ref=ref, script=script.name):
                            create = Mock(return_value=response)
                            client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
                            with patch.dict(sys.modules, {'openai': SimpleNamespace(OpenAI=lambda: client)}), \
                                 patch.dict(os.environ, {'AITRAINER_ASSET_REF': ref}), \
                                 patch.object(sys, 'argv', [str(script), 'https://example.com/input.jpg']), \
                                 patch('builtins.input', return_value='https://example.com/input.jpg'), \
                                 contextlib.redirect_stdout(io.StringIO()):
                                if ref == 'main':
                                    os.environ.pop('AITRAINER_ASSET_REF')
                                result = runpy.run_path(str(script), run_name='__main__')
                            self.assertIn('/refs/heads/'+ref+'/data/', result['url_head'])
                            self.assertTrue(create.called)
                            for call in create.call_args_list:
                                for message in call.kwargs['messages']:
                                    if not isinstance(message['content'], list):
                                        continue
                                    for content in message['content']:
                                        if content['type'] != 'image_url':
                                            continue
                                        url = content['image_url']['url']
                                        if 'raw.githubusercontent.com' in url:
                                            relative = unquote(url.split('/'+ref+'/', 1)[1])
                                            self.assertTrue((root/relative).is_file(), relative)

    def test_mediapipe_keeps_its_dataset(self):
        script = root/'experiments/mediapipe/app.py'
        for cwd in (root, root.parent):
            capture = Mock(return_value=SimpleNamespace(read=lambda: (False, None), release=lambda: None))
            cv2 = SimpleNamespace(VideoCapture=capture, destroyAllWindows=lambda: None)
            pose = SimpleNamespace(poseDetector=lambda **kwargs: None)
            with contextlib.chdir(cwd), \
                 patch.dict(sys.modules, {'cv2': cv2, 'pose_module': pose}), \
                 contextlib.redirect_stdout(io.StringIO()):
                runpy.run_path(str(script), run_name='__main__')
            self.assertEqual(capture.call_count, 40)
            for call in capture.call_args_list:
                path = Path(call.args[0])
                self.assertTrue(path.is_relative_to(script.parent/'squat_img'))
                self.assertTrue(path.is_file(), str(path))


if __name__ == '__main__':
    unittest.main()

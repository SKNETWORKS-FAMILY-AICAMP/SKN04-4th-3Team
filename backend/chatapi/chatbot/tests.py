# tests.py
import unittest
from chatbot import process_user_input

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        """
        각 테스트 케이스를 실행하기 전에 호출됩니다.
        테스트에 필요한 초기 설정을 수행합니다.
        """
        self.session_store = {}
        self.session_id = "test_session"
        self.user_input = "해외여행 보험에 대해 알고 싶어요."

    def test_process_user_input(self):
        """
        process_user_input 함수가 올바르게 작동하는지 테스트합니다.
        """
        response = process_user_input(self.user_input, self.session_store, self.session_id)
        print(f"Input: {self.user_input}")
        print(f"Response: {response}")
        self.assertIsNotNone(response)  # 응답이 None이 아닌지 확인합니다.
        self.assertIsInstance(response, str)  # 응답이 문자열인지 확인합니다.
        self.assertGreater(len(response), 0)  # 응답의 길이가 0보다 큰지 확인합니다.

    def test_session_history(self):
        """
        세션 히스토리가 올바르게 기록되는지 테스트합니다.
        """
        process_user_input(self.user_input, self.session_store, self.session_id)
        print(f"Session ID: {self.session_id}")
        print(f"Session History: {self.session_store[self.session_id].messages}")
        self.assertIn(self.session_id, self.session_store)  # 세션 ID가 세션 저장소에 있는지 확인합니다.
        self.assertGreater(len(self.session_store[self.session_id].messages), 0)  # 세션 히스토리의 메시지 수가 0보다 큰지 확인합니다.

if __name__ == '__main__':
    unittest.main()
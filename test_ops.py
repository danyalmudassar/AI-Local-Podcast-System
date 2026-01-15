import unittest
from podcast_agent import search_tool, local_llm

class TestPodcastAgent(unittest.TestCase):
    def test_search_tool(self):
        print("\nTesting Search Tool...")
        result = search_tool.run("latest AI news")
        print(f"Search Result: {result[:100]}...")
        self.assertTrue(len(result) > 10, "Search tool should return some results")
        self.assertNotIn("Search failed", result, "Search tool should not fail")

    def test_llm_connectivity(self):
        print("\nTesting LLM Connectivity...")
        response = local_llm.invoke("Say 'Test Successful'")
        print(f"LLM Response: {response}")
        self.assertTrue(len(response) > 0, "LLM should return a response")

if __name__ == '__main__':
    unittest.main()

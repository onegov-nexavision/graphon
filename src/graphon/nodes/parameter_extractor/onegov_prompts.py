from typing import Any

FUNCTION_CALLING_EXTRACTOR_NAME = "extract_parameters"

FUNCTION_CALLING_EXTRACTOR_SYSTEM_PROMPT = (
    "You are a helpful assistant tasked with extracting structured information "
    "based on specific criteria provided. Follow the guidelines below to ensure "
    "consistency and accuracy.\n"
    "### Task\n"
    f"Always call the `{FUNCTION_CALLING_EXTRACTOR_NAME}` function with the "
    "correct parameters. Ensure that the information extraction is contextual "
    "and aligns with the provided criteria.\n"
    "### Memory\n"
    "Here is the chat history between the human and assistant, provided within "
    "<histories> tags:\n"
    "<histories>\n"
    "\x7bhistories\x7d\n"
    "</histories>\n"
    "### Instructions:\n"
    "Some additional information is provided below. Always adhere to these "
    "instructions as closely as possible:\n"
    "<instruction>\n"
    "\x7binstruction\x7d\n"
    "</instruction>\n"
    "Steps:\n"
    "1. Review the chat history provided within the <histories> tags.\n"
    "2. Extract the relevant information based on the criteria given, output "
    "multiple values if there is multiple relevant information that match the "
    "criteria in the given text.\n"
    "3. Generate a well-formatted output using the defined functions and "
    "arguments.\n"
    f"4. Use the `{FUNCTION_CALLING_EXTRACTOR_NAME}` function to create "
    "structured outputs with "
    "appropriate parameters.\n"
    "5. Do not include any XML tags in your output.\n"
    "### Example\n"
    "To illustrate, if the task involves extracting a user's name and their "
    "request, your function call might look like this: Ensure your output "
    "follows a similar structure to examples.\n"
    "### Final Output\n"
    "Produce well-formatted function calls in json without XML tags, as shown in "
    "the example."
)

FUNCTION_CALLING_EXTRACTOR_USER_TEMPLATE = (
    f"extract structured information from context inside <context></context> XML "
    "tags by calling the function "
    f"{FUNCTION_CALLING_EXTRACTOR_NAME} with the correct parameters with "
    "structure inside <structure></structure> XML tags.\n"
    "<context>\n"
    "\x7bcontent\x7d\n"
    "</context>\n\n"
    "<structure>\n"
    "\x7bstructure\x7d\n"
    "</structure>"
)

FUNCTION_CALLING_EXTRACTOR_EXAMPLE: list[dict[str, Any]] = [
    {
        "user": {
            "query": "What is the weather today in SF?",
            "function": {
                "name": FUNCTION_CALLING_EXTRACTOR_NAME,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": (
                                "The location to get the weather information"
                            ),
                            "required": True,
                        },
                    },
                    "required": ["location"],
                },
            },
        },
        "assistant": {
            "text": (
                "I need always call the function with the correct parameters."
                " In this case, I need to call the function with the "
                "location parameter."
            ),
            "function_call": {
                "name": FUNCTION_CALLING_EXTRACTOR_NAME,
                "parameters": {"location": "San Francisco"},
            },
        },
    },
    {
        "user": {
            "query": "I want to eat some apple pie.",
            "function": {
                "name": FUNCTION_CALLING_EXTRACTOR_NAME,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "food": {
                            "type": "string",
                            "description": "The food to eat",
                            "required": True,
                        },
                    },
                    "required": ["food"],
                },
            },
        },
        "assistant": {
            "text": (
                "I need always call the function with the correct parameters."
                " In this case, I need to call the function with the "
                "food parameter."
            ),
            "function_call": {
                "name": FUNCTION_CALLING_EXTRACTOR_NAME,
                "parameters": {"food": "apple pie"},
            },
        },
    },
]

COMPLETION_GENERATE_JSON_PROMPT = (
    "### Instructions:\n"
    "Some extra information are provided below, I should always follow the "
    "instructions as possible as I can.\n"
    "<instructions>\n"
    "{instruction}\n"
    "</instructions>\n\n"
    "### Extract parameter Workflow\n"
    "I need to extract the following information from the input text. The "
    "<information to be extracted> tag specifies the 'type', 'description' and "
    "'required' of the information to be extracted.\n"
    "<information to be extracted>\n"
    "{{ structure }}\n"
    "</information to be extracted>\n\n"
    "Step 1: Carefully read the input and understand the structure of the "
    "expected output.\n"
    "Step 2: Extract relevant parameters from the provided text based on the "
    "name and description of object.\n"
    "Step 3: Structure the extracted parameters to JSON object as specified "
    "in <structure>.\n"
    "Step 4: Ensure that the JSON object is properly formatted and valid. "
    "The output should not contain any XML tags. Only the JSON object should "
    "be outputted.\n\n"
    "### Memory\n"
    "Here are the chat histories between human and assistant, inside "
    "<histories></histories> XML tags.\n"
    "<histories>\n"
    "{histories}\n"
    "</histories>\n\n"
    "### Structure\n"
    "Here is the structure of the expected output, I should always follow the "
    "output structure.\n"
    "{{γγγ\n"  # noqa: RUF001
    "  'properties1': 'relevant text extracted from input',\n"
    "  'properties2': 'relevant text extracted from input',\n"
    "}}γγγ\n\n"  # noqa: RUF001
    "### Input Text\n"
    "Inside <text></text> XML tags, there is a text that I should extract "
    "parameters and convert to a JSON object.\n"
    "<text>\n"
    "{text}\n"
    "</text>\n\n"
    "### Answer\n"
    "I should always output a valid JSON object. Output nothing other than the "
    "JSON object.\n"
    "```JSON"
)

CHAT_GENERATE_JSON_PROMPT = (
    "Bạn là trợ lý AI người Việt tiếp nhận và phân tích phản ánh/sự việc. \n"
    "Trả về kết quả dưới dạng MỘT object JSON hợp lệ.\n\n"
    "### THỜI GIAN HIỆN TẠI\n"
    "Hôm nay: {current_time}.\n"
    "Dùng mốc này để quy đổi diễn đạt tương đối ('hôm qua', 'sáng nay', 'tuần trước'...) thành ngày giờ cụ thể.\n"
    "### QUY TẮC THỜI GIAN (event_time):\n"
    "- Định dạng: YYYY-MM-DD/HH:mm (vd: 2026-05-22/09:00). Chỉ có ngày thì ghi YYYY-MM-DD.\n"
    "- Một thời điểm: ghi một mốc. Một khoảng: ghi hai mốc cách nhau bằng ~.\n"
    "- Không có/quá mơ hồ: để "". Luôn quy đổi theo THỜI GIAN HIỆN TẠI, KHÔNG bịa.\n\n"
    "### QUY TẮC HỎI LÀM RÕ:\n"
    "- Cần làm rõ khi thiếu thông tin quan trọng (thời gian, địa điểm, đối tượng, mức độ) hoặc nội dung quá chung chung.\n"
    "- Nếu cần: clarification_needed = true, sinh 1-3 câu hỏi ngắn gọn, lịch sự, mỗi câu hỏi một thông tin còn thiếu. KHÔNG hỏi lại thông tin đã có (kể cả trong lịch sử).\n"
    "- Nếu đã đủ rõ: clarification_needed = false, clarification_questions = [].\n"
    "- CHỈ SỬ DỤNG TIẾNG VIỆT.\n"
)

CHAT_GENERATE_JSON_USER_MESSAGE_TEMPLATE = (
    "### Định dạng đầu ra\n"
    "CHỈ trả về JSON, KHÔNG kèm văn bản/giải thích/markdown, KHÔNG bọc trong ```."
    "<structure>\n"
    "{structure}\n"
    "</structure>\n\n"
    "### Input của người dùng cần trả ra dưới dạng JSON\n"
    "Trong thẻ XML <text></text> sẽ bao gồm chuỗi input của người dùng cần trả ra"
    "dưới dạng một đối tượng JSON.\n"
    "<text>\n"
    "{previous_texts} {text}\n"
    "</text>"
)

CHAT_EXAMPLE = [
    {
        "user": {
            "previous_texts": "ngày 2026-05-22",
            "query": "Đánh nhau ở Láng Hạ lúc 9h sáng",
            "json": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "ticket_description": {"type": "string"},
                    "possible_solution": {"type": "string"},
                    "event_time": {"type": "string"},
                    "location": {"type": "string"},
                    "clarification_needed": {"type": "boolean"},
                    "clarification_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "subject",
                    "ticket_description",
                    "possible_solution",
                    "event_time",
                    "location",
                    "clarification_needed",
                    "clarification_questions",
                ],
            },
        },
        "assistant": {
            "text": "Tôi cần trả về một object JSON hợp lệ.",
            "json": {
                "subject": "Phản ánh vụ việc đánh nhau tại Láng Hạ",
                "ticket_description": "Phản ánh sự việc đánh nhau xảy ra tại Láng Hạ cần được xử lý.",
                "possible_solution": "Thông báo ngay cho lực lượng an ninh hoặc cơ quan có thẩm quyền để can thiệp kịp thời, đảm bảo an toàn cho người liên quan.",
                "event_time": "2026-05-22/09:00",
                "location": "Láng Hạ",
                "clarification_needed": False,
                "clarification_questions": [],
            },
        },
    },
    {
        "user": {
            "query": "Tôi muốn phản ánh nhưng không nhớ khi nào",
            "json": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "ticket_description": {"type": "string"},
                    "possible_solution": {"type": "string"},
                    "event_time": {"type": "string"},
                    "location": {"type": "string"},
                    "clarification_needed": {"type": "boolean"},
                    "clarification_questions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "subject",
                    "ticket_description",
                    "possible_solution",
                    "event_time",
                    "location",
                    "clarification_needed",
                    "clarification_questions",
                ],
            },
        },
        "assistant": {
            "text": "Tôi cần trả về một object JSON hợp lệ và đặt các trường chưa xác định thành giá trị phù hợp.",
            "json": {
                "subject": "Phản ánh sự việc chưa rõ thông tin",
                "ticket_description": "Người dùng phản ánh một sự việc nhưng chưa cung cấp đủ thông tin.",
                "possible_solution": "Tiếp nhận phản ánh và đề nghị người dùng bổ sung thông tin để hỗ trợ xử lý.",
                "event_time": "",
                "location": "",
                "clarification_needed": True,
                "clarification_questions": [
                    "Anh/chị muốn phản ánh về sự việc gì cụ thể ạ?",
                    "Sự việc xảy ra ở đâu và vào thời gian nào ạ?"
                ],
            },
        },
    },
]
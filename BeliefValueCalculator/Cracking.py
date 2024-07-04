from transformers import BartForConditionalGeneration, BertTokenizer
import torch
import re

class Cracking(object):

    def init(self):
        self.model_path = "D:\my_finetuned_bart_model_2_for20"  # 模型所在的路径
        self.tokenizer = BertTokenizer.from_pretrained(self.model_path)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_path).to(
            "cuda" if torch.cuda.is_available() else "cpu")

    def remove_citations(self,text):
        citation_patterns = [
            r'\[\d+\]',  # 匹配形如 [1], [2], ...
            r'\(\d+\)',  # 匹配形如 (1), (2), ...

        ]
        for pattern in citation_patterns:
            text = re.sub(pattern, '', text)
        return text

    def clean_title(self,title):
        """清理标题，去除 '_百度百科' 及词条末尾的括号及其内容"""
        # 去除 '_百度百科'
        title = title.replace('_百度百科', '').strip()
        # 查找并移除末尾的括号及其内容（包括圆括号和方括号）
        title = re.sub(r'[（\[](.*?[）\]])$', '', title)
        return title

    def process_and_format_text(self,text,title):
        """处理文本并格式化为指定输出格式"""
        cleaned_text = self.remove_citations(text)
        sentences = re.split(r'(?<=[。！？])', cleaned_text)
        formatted_output = [f'{{"Input": "{title}, {s.strip()}"}},' for s in sentences if s.strip()]
        return formatted_output


    def generate_text(self,input_text):
            output_text = []
            # 确保去除可能的'Input'前缀
            clean_input_text = input_text.replace("Input", "").strip()

            inputs = self.tokenizer(clean_input_text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(
                self.model.device)
            with torch.no_grad():
                generated_ids = self.model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"],
                    max_new_tokens=500)

            pred_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

            split_words = pred_text.strip("").split("||")

            result = []
            for word in split_words:
                word = word.replace(" ","")
                result.append(word)

            return result

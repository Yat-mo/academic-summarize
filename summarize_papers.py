import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

def extract_text_from_pdf(pdf_path, max_chars=10000):
    """从PDF文件中提取文本，支持按字数限制"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        text = ''
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        
        text = text.strip()
        return text, total_pages

def split_text_by_chars(text, max_chars=10000):
    """将文本按指定字数分割"""
    parts = []
    for i in range(0, len(text), max_chars):
        parts.append(text[i:i+max_chars])
    return parts

def summarize_with_openai(text_part, total_pages, part_index, total_parts):
    """使用OpenAI API总结文本部分"""
    try:
        system_prompt = f"你是一个学术论文总结专家。论文共{total_pages}页，这是第{part_index+1}/{total_parts}部分文本。请用中文总结这部分内容的主要信息。如果这部分内容不完整，请说明。使用markdown格式输出。"
        
        response = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_part}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用OpenAI API时出错: {str(e)}")
        return None

def process_papers(max_chars=10000):
    """处理所有PDF论文"""
    input_dir = "论文输入区"
    output_dir = "论文总结区"
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有PDF文件
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("未找到PDF文件。请将PDF文件放入'论文输入区'文件夹中。")
        return
    
    for pdf_file in pdf_files:
        print(f"\n正在处理: {pdf_file}")
        
        # 提取PDF全文
        pdf_path = os.path.join(input_dir, pdf_file)
        full_text, total_pages = extract_text_from_pdf(pdf_path)
        
        if not full_text.strip():
            print(f"警告: {pdf_file} 中未提取到文本内容")
            continue
        
        # 按字数分割文本
        text_parts = split_text_by_chars(full_text, max_chars)
        total_parts = len(text_parts)
        
        # 存储各部分总结
        all_summaries = []
        
        # 逐部分总结
        for i, text_part in enumerate(text_parts):
            print(f"正在生成第{i+1}/{total_parts}部分总结...")
            summary = summarize_with_openai(text_part, total_pages, i, total_parts)
            
            if summary:
                all_summaries.append(summary)
            
            # 添加延迟以避免API限制
            time.sleep(2)
        
        # 合并所有部分总结
        if all_summaries:
            # 创建输出文件
            output_filename = os.path.splitext(pdf_file)[0] + '.md'
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {pdf_file} 论文总结\n\n")
                f.write("## 总体概述\n\n")
                
                # 添加总结概述
                overview_prompt = f"以下是论文的{total_parts}个部分的总结。请提供一个整体概述，包括研究目的、方法、主要发现和结论。"
                overview_response = client.chat.completions.create(
                    model="gpt-4o-2024-05-13",
                    messages=[
                        {"role": "system", "content": "你是一个学术论文总结专家。"},
                        {"role": "user", "content": overview_prompt + "\n\n" + "\n\n".join(all_summaries)}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                overview = overview_response.choices[0].message.content
                f.write(overview + "\n\n")
                
                # 添加各部分详细总结
                f.write("## 分部分总结\n\n")
                for i, summary in enumerate(all_summaries, 1):
                    f.write(f"### 部分 {i}\n\n")
                    f.write(summary + "\n\n")
            
            print(f"总结已保存到: {output_filename}")
        else:
            print(f"无法为 {pdf_file} 生成总结")

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("错误: 未找到OPENAI_API_KEY环境变量。请在.env文件中设置您的API密钥。")
    else:
        print("开始处理论文...")
        process_papers()
        print("\n所有论文处理完成！")

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

def summarize_with_openai(text_part, total_pages, part_index, total_parts, all_text_parts):
    """使用OpenAI API总结文本部分"""
    try:
        # 准备上下文信息
        previous_parts = all_text_parts[:part_index]
        next_parts = all_text_parts[part_index+1:]
        
        # 为每个部分提供更多上下文信息的系统提示
        system_prompt = f"""
        你是一个学术论文总结专家。论文共{total_pages}页，这是第{part_index+1}/{total_parts}部分文本。
        
        总结要求：
        1. 准确描述本部分的具体内容和技术细节
        2. 解释本部分在论文整体叙事中的具体作用
        3. 阐明本部分与前后部分的逻辑关联
        4. 使用专业且生动的学术语言
        5. 避免使用空洞的描述性词语
        6. 突出研究的独特方法和具体实现
        
        特别注意：
        - 详细说明研究方法、实验设计、数据处理等具体环节
        - 解释技术细节和算法实现
        - 展示研究的创新性和实践价值
        """
        
        # 为每个部分添加上下文关联的用户提示
        context_aware_prompt = f"""
        请仔细分析这部分文本（第{part_index+1}/{total_parts}部分）。
        
        上下文信息：
        - 前序部分概要：{' | '.join([f"第{i+1}部分摘要" for i in range(len(previous_parts))])}
        - 后续部分概要：{' | '.join([f"第{part_index+i+2}部分摘要" for i in range(len(next_parts))])}
        
        分析和总结时，请特别注意：
        1. 具体描述本部分的研究内容
        2. 解释本部分如何连接前后部分
        3. 突出研究方法的技术细节
        4. 使用具体的例子和数据说明研究过程
        5. 展示研究的创新性和实践意义
        
        文本内容如下：
        {text_part}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context_aware_prompt}
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
    try:
        input_dir = "论文输入区"
        output_dir = "论文总结区"
        
        # 检查并创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取所有PDF文件
        pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("未找到PDF文件。请将PDF文件放入'论文输入区'文件夹中。")
            return
        
        print("\n开始处理论文...\n")
        
        # 处理每个PDF文件
        for pdf_file in pdf_files:
            try:
                print(f"\n正在处理: {pdf_file}")
                
                # 读取PDF文件
                pdf_path = os.path.join(input_dir, pdf_file)
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                
                print(f"正在分析文本...")
                
                # 分割文本
                text_parts = split_text_by_chars(text, max_chars)
                total_parts = len(text_parts)
                total_pages = len(pdf_reader.pages)
                
                # 处理每个部分
                all_summaries = []
                for i, part in enumerate(text_parts):
                    print(f"\r正在生成第{i+1}/{total_parts}部分总结...", end="", flush=True)
                    summary = summarize_with_openai(part, total_pages, i, total_parts, text_parts)
                    if summary:
                        all_summaries.append(summary)
                print()  # 换行
                
                print(f"正在生成整体概述...")
                
                # 生成总体概述
                overview_prompt = f"""
                以下是论文的{total_parts}个部分的总结。请提供一个整体概述，要求：
                1. 综合每个部分的关键信息
                2. 突出论文的主要研究目的、方法、发现和结论
                3. 保持逻辑连贯性和层次清晰
                4. 字数控制在500-800字之间
                
                各部分总结如下：
                """
                
                overview = client.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages=[
                        {"role": "system", "content": "你是一个专业的学术论文总结专家，擅长提炼论文精髓。"},
                        {"role": "user", "content": overview_prompt + "\n\n" + "\n\n".join(all_summaries)}
                    ]
                ).choices[0].message.content
                
                # 生成最终结论
                print(f"正在生成最终结论...")
                final_conclusion_prompt = f"""
                基于以下论文总结和整体概述，请提供一个极其精炼的结论。要求：
                1. 高度概括论文的核心价值和意义
                2. 突出研究的创新点和潜在影响
                3. 字数控制在500-1000字
                4. 语言要详细、有力、学术
                
                整体概述：
                {overview}
                
                各部分详细总结：
                {chr(10).join(all_summaries)}
                """
                
                final_conclusion = client.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages=[
                        {"role": "system", "content": "你是一个擅长提炼学术论文核心价值的专家。"},
                        {"role": "user", "content": final_conclusion_prompt}
                    ]
                ).choices[0].message.content
                
                # 保存总结
                output_file = os.path.join(output_dir, os.path.splitext(pdf_file)[0] + '.md')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {pdf_file} 论文总结\n\n")
                    f.write("## 整体概述\n\n")
                    f.write(overview + "\n\n")
                    f.write("## 详细总结\n\n")
                    for i, summary in enumerate(all_summaries):
                        f.write(f"### 第{i+1}部分\n\n")
                        f.write(summary + "\n\n")
                    f.write("## 结论\n\n")
                    f.write(final_conclusion + "\n\n")
                
                print(f"总结已保存到: {output_file}\n")
                
            except Exception as e:
                print(f"处理 {pdf_file} 时出错: {str(e)}")
                continue
        
        print("\n所有论文处理完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("错误: 未找到OPENAI_API_KEY环境变量。请在.env文件中设置您的API密钥。")
    else:
        print("开始处理论文...")
        process_papers()
        print("\n所有论文处理完成！")

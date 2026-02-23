from google import genai
import os 
from dotenv import load_dotenv
import json

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt_text="""あなたはプロの料理研究家です。

以下の条件に従ってレシピを生成してください。

【重要】
・出力はJSONのみ
・説明文は禁止
・コードブロックは禁止
・JSON以外の文字を一切出力しないこと

【生成条件】
・日本語で出力
・単位は「大さじ」「小さじ」「ひとつまみ」「適量」など自然な日本語表記
・レシピは必ず1件生成
・材料不足は最大2つまで許容
・どうしても作れない場合は以下の形式で出力：

{"error": "レシピを生成できません"}

【JSON形式】

{
  "recipes": [
    {
      "title": "料理名",
      "material": "材料を改行区切りで記載",
      "recipe_text": "手順を番号付きで改行区切りで記載",
      "genre": "和食/洋食/中華など",
      "category": "主菜/副菜/デザートなど"
    }
  ]
}

必ず上記形式に厳密に従うこと。
"""

async def gemini(user_input:str):
    print(user_input)
    full_prompt = prompt_text + user_input
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = full_prompt,
    )
    print(response.text)
    
    try:
        return json.loads(response.text)
    except:
        return{"error": "JSON parse error"}

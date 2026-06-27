#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日天气邮件发送脚本
获取重庆天气并通过 QQ 邮箱发送
"""

import os
import sys
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import urllib.request
import urllib.error

# 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "495962397@qq.com"
SENDER_PASSWORD = os.environ.get("QQ_MAIL_PASSWORD", "")
RECEIVER_EMAIL = "495962397@qq.com"
CITY = "Chongqing"


def get_weather():
    """获取天气信息"""
    try:
        url = f"https://wttr.in/{CITY}?format=j1&lang=zh"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        current = data['current_condition'][0]
        today = data['weather'][0]
        
        # 天气代码映射
        weather_desc_en = current['weatherDesc'][0]['value']
        weather_desc_zh = translate_weather(weather_desc_en)
        
        weather_info = {
            'city': '重庆',
            'date': datetime.now().strftime('%Y年%m月%d日'),
            'weekday': get_weekday(),
            'current_temp': current['temp_C'],
            'feels_like': current['FeelsLikeC'],
            'description': weather_desc_zh,
            'max_temp': today['maxtempC'],
            'min_temp': today['mintempC'],
            'humidity': current['humidity'],
            'wind_speed': current['windspeedKmph'],
            'wind_dir': current['winddir16Point'],
            'visibility': current['visibility'],
            'uv_index': current['uvIndex'],
            'sunrise': today['astronomy'][0]['sunrise'],
            'sunset': today['astronomy'][0]['sunset'],
        }
        
        return weather_info
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None


def translate_weather(desc_en):
    """简单的天气描述翻译"""
    translations = {
        'Clear': '晴',
        'Sunny': '晴',
        'Partly cloudy': '多云',
        'Cloudy': '阴',
        'Overcast': '阴',
        'Mist': '薄雾',
        'Fog': '雾',
        'Light rain': '小雨',
        'Moderate rain': '中雨',
        'Heavy rain': '大雨',
        'Light snow': '小雪',
        'Moderate snow': '中雪',
        'Heavy snow': '大雪',
        'Thundery outbreaks possible': '可能有雷暴',
        'Patchy rain nearby': '局部有雨',
        'Light drizzle': '毛毛雨',
        'Freezing drizzle': '冻雨',
        'Heavy drizzle': '大毛雨',
        'Light sleet': '小霰',
        'Moderate or heavy sleet': '中或大霰',
        'Light snow showers': '小阵雪',
        'Moderate or heavy snow showers': '中或大阵雪',
        'Light showers': '小阵雨',
        'Heavy showers': '大阵雨',
        'Light rain shower': '小阵雨',
        'Moderate or heavy rain shower': '中或大阵雨',
        'Torrential rain shower': '暴雨',
        'Thunderstorm': '雷暴',
        'Blizzard': '暴风雪',
        'Blowing snow': '风吹雪',
    }
    return translations.get(desc_en, desc_en)


def get_weekday():
    """获取中文星期"""
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[datetime.now().weekday()]


def get_clothing_suggestion(weather):
    """根据天气给出穿衣建议"""
    current_temp = int(weather['current_temp'])
    description = weather['description']
    
    suggestions = []
    
    if current_temp >= 30:
        suggestions.append("🌡️ 天气炎热，建议穿短袖、短裤等清凉夏装")
    elif current_temp >= 25:
        suggestions.append("🌡️ 天气较热，建议穿T恤、薄长裤")
    elif current_temp >= 20:
        suggestions.append("🌡️ 温度适宜，建议穿长袖衬衫或薄外套")
    elif current_temp >= 15:
        suggestions.append("🌡️ 天气偏凉，建议穿外套或薄毛衣")
    elif current_temp >= 10:
        suggestions.append("🌡️ 天气较冷，建议穿厚外套或毛衣")
    else:
        suggestions.append("🌡️ 天气寒冷，建议穿羽绒服或厚棉衣")
    
    if '雨' in description:
        suggestions.append("☔ 今天有雨，记得带伞！")
    if '雪' in description:
        suggestions.append("❄️ 今天有雪，注意防寒防滑")
    if '雾' in description or '霾' in description:
        suggestions.append("🌫️ 今天有雾/霾，注意交通安全，佩戴口罩")
    if int(weather['uv_index']) >= 6:
        suggestions.append("☀️ 紫外线较强，外出注意防晒")
    
    return suggestions


def get_travel_suggestion(weather):
    """出行建议"""
    description = weather['description']
    wind_speed = int(weather['wind_speed'])
    
    if '雨' in description or '雪' in description or '雾' in description:
        return "⚠️ 今天天气不佳，如需外出请注意安全，建议减速慢行"
    elif wind_speed > 30:
        return "🌬️ 今天风力较大，外出注意防风，远离广告牌等高空物品"
    else:
        return "✅ 今天天气不错，适合外出活动！"


def create_email_content(weather):
    """创建邮件内容"""
    clothing = get_clothing_suggestion(weather)
    travel = get_travel_suggestion(weather)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .weather-main {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .temperature {{
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            .weather-desc {{
                font-size: 20px;
                color: #666;
            }}
            .details {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin: 20px 0;
            }}
            .detail-item {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .detail-label {{
                font-size: 12px;
                color: #999;
                margin-bottom: 5px;
            }}
            .detail-value {{
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }}
            .suggestions {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .suggestions h3 {{
                margin-top: 0;
                color: #667eea;
            }}
            .suggestions ul {{
                margin: 10px 0;
                padding-left: 20px;
            }}
            .suggestions li {{
                margin: 8px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #999;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌤️ 小鱼干先生早上好！</h1>
            <p>现在为您带来重庆天气</p>
        </div>
        
        <div class="content">
            <div class="weather-main">
                <div class="weather-desc">{weather['date']} {weather['weekday']}</div>
                <div class="temperature">{weather['current_temp']}°C</div>
                <div class="weather-desc">{weather['description']}</div>
            </div>
            
            <div class="details">
                <div class="detail-item">
                    <div class="detail-label">🌡️ 体感温度</div>
                    <div class="detail-value">{weather['feels_like']}°C</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">📊 今日温度</div>
                    <div class="detail-value">{weather['min_temp']}° ~ {weather['max_temp']}°</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">💧 湿度</div>
                    <div class="detail-value">{weather['humidity']}%</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">💨 风速</div>
                    <div class="detail-value">{weather['wind_speed']} km/h</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">👁️ 能见度</div>
                    <div class="detail-value">{weather['visibility']} km</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">☀️ 紫外线</div>
                    <div class="detail-value">{weather['uv_index']}</div>
                </div>
            </div>
            
            <div class="suggestions">
                <h3>📝 温馨提示</h3>
                <ul>
                    {''.join(f'<li>{s}</li>' for s in clothing)}
                    <li>{travel}</li>
                </ul>
            </div>
            
            <div class="suggestions">
                <h3>🌅 日出日落</h3>
                <p>日出时间：{weather['sunrise']} | 日落时间：{weather['sunset']}</p>
            </div>
            
            <div class="footer">
                <p>祝你有美好的一天！😊</p>
                <p style="font-size: 12px; margin-top: 20px;">本邮件由 WorkBuddy 自动发送</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


def send_email(weather_info):
    """发送邮件"""
    if not SENDER_PASSWORD:
        print("错误：未设置 QQ_MAIL_PASSWORD 环境变量")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"重庆今日天气 - {weather_info['date']}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    html_content = create_email_content(weather_info)
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ 邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("每日天气邮件发送任务")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 获取天气
    print("\n📡 正在获取重庆天气...")
    weather_info = get_weather()
    
    if not weather_info:
        print("❌ 获取天气失败，任务终止")
        sys.exit(1)
    
    print(f"✅ 天气获取成功")
    print(f"   城市: {weather_info['city']}")
    print(f"   天气: {weather_info['description']}")
    print(f"   温度: {weather_info['current_temp']}°C")
    
    # 发送邮件
    print("\n📧 正在发送邮件...")
    success = send_email(weather_info)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 任务完成！")
        print("=" * 50)
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("❌ 任务失败！")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()

import os
import urllib.request

# 规则源列表 (统一采用 blackmatrix7 的 Clash .list 源)
SOURCES = {
    "Advertising": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Advertising/Advertising.list",
    "OpenAI": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list",
    "Spotify": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Spotify/Spotify.list",
    "Facebook": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Facebook/Facebook.list",
    "Instagram": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Instagram/Instagram.list",
    "ChinaMax": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ChinaMax/ChinaMax.list"
}

# Anywhere 允许的标准前缀
VALID_PREFIXES = ("DOMAIN-SUFFIX,", "DOMAIN-KEYWORD,", "DOMAIN,", "IP-CIDR,", "IP-CIDR6,")

def clean_and_format(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    for prefix in VALID_PREFIXES:
        if line.startswith(prefix):
            parts = line.split(",")
            return f"{parts[0]},{parts[1]}"
    return None

def main():
    os.makedirs("rules", exist_ok=True)
    
    for name, url in SOURCES.items():
        print(f"正在处理: {name}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode('utf-8')
            
            seen = set()
            rules = []
            for line in content.splitlines():
                rule = clean_and_format(line)
                if rule and rule not in seen:
                    seen.add(rule)
                    rules.append(rule)
            
            output_file = os.path.join("rules", f"{name}.arrs")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(rules) + "\n")
            print(f"导出成功: {output_file} (包含 {len(rules)} 条有效规则)")
            
        except Exception as e:
            print(f"处理 {name} 失败: {e}")

if __name__ == "__main__":
    main()

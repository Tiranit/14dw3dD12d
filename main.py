import os
import ccxt
import smtplib
import numpy as np
import pandas as pd
import mplfinance as mpf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 🔹 اطلاعات ایمیل (از متغیرهای محیطی GitHub Secrets)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# 🔹 صرافی KuCoin
exchange = ccxt.bybit()

# 🔹 لیست ارزهای موردنظر
symbols = ['BTC/USDT', 'XRP/USDT', 'ETH/USDT', 'USDC/USDT', 'DOGE/USDT', 'SOL/USDT', 'HBAR/USDT', 'LTC/USDT', 'SUI/USDT', 'PEPE/USDT', 'ADA/USDT', 'SOLV/USDT', 'BNB/USDT', 'XLM/USDT', 'SHIB/USDT', 'ENA/USDT', 'TRX/USDT', 'LINK/USDT', 'AIXBT/USDT', 'PNUT/USDT', 'WIF/USDT', 'WLD/USDT', 'RUNE/USDT', 'ALGO/USDT', 'AVAX/USDT', 'NEIRO/USDT', 'EOS/USDT', 'VET/USDT', 'NEAR/USDT', 'SAND/USDT', 'MOVE/USDT', 'BONK/USDT', 'FET/USDT', 'APT/USDT', 'DOT/USDT', 'FIL/USDT', 'AAVE/USDT', 'UNI/USDT', 'TAO/USDT', 'FLOKI/USDT', 'USUAL/USDT', 'CRV/USDT', 'PHA/USDT', 'TIA/USDT', 'AMP/USDT', 'PENGU/USDT', 'ARB/USDT', 'INJ/USDT', 'CGPT/USDT', 'SEI/USDT', 'IOTA/USDT', 'BCH/USDT', 'RENDER/USDT', 'ZEN/USDT', 'OP/USDT', 'BIO/USDT', 'TON/USDT', 'JASMY/USDT', 'GMT/USDT', 'ICP/USDT', 'ATOM/USDT', 'PENDLE/USDT', 'ETC/USDT', 'RAY/USDT', 'KDA/USDT', 'RSR/USDT', 'BOME/USDT', 'POL/USDT', 'CFX/USDT', 'GRT/USDT', 'VANA/USDT', 'ZRO/USDT', 'IO/USDT', 'ETHFI/USDT', 'STX/USDT', 'ENS/USDT', 'WBTC/USDT', 'COOKIE/USDT', 'TURBO/USDT', 'DYDX/USDT', 'ZK/USDT', 'SUSHI/USDT', 'JUP/USDT', 'BLZ/USDT', 'LDO/USDT', 'ORDI/USDT', 'NOT/USDT', 'EIGEN/USDT', 'OM/USDT', 'THETA/USDT', 'AR/USDT', 'NEO/USDT', 'COW/USDT', 'APE/USDT', 'MANA/USDT', 'MKR/USDT', 'KAIA/USDT', 'CAKE/USDT', 'ARKM/USDT', 'STRK/USDT', 'MEME/USDT', 'EDU/USDT', 'BAL/USDT', 'XAI/USDT', 'CHZ/USDT', 'MANTA/USDT', 'DASH/USDT', 'FTT/USDT', 'BLUR/USDT', 'PROM/USDT', 'SUPER/USDT', 'EGLD/USDT', 'ROSE/USDT', 'ONE/USDT', 'CETUS/USDT', 'LPT/USDT', 'AGLD/USDT', 'FIDA/USDT', 'XTZ/USDT', 'ALT/USDT', 'LUMIA/USDT', 'W/USDT', 'JTO/USDT', 'AXS/USDT', 'LUNC/USDT', 'PYR/USDT', 'COMP/USDT', 'PEOPLE/USDT', 'ME/USDT', 'DOGS/USDT', 'ZRX/USDT', 'PYTH/USDT', 'LUNA/USDT', 'LQTY/USDT', 'QNT/USDT', 'STG/USDT', 'SNX/USDT', 'BB/USDT', 'IOST/USDT', 'ASTR/USDT', 'TRB/USDT', 'SSV/USDT', 'ZIL/USDT', 'PIXEL/USDT', 'MINA/USDT', 'PORTAL/USDT', 'LISTA/USDT', 'IMX/USDT', 'YFI/USDT', 'CELO/USDT', 'ACX/USDT', 'DEXE/USDT', 'WOO/USDT', '1INCH/USDT', 'CKB/USDT', 'FLOW/USDT', 'SCR/USDT', 'ATA/USDT', 'AEVO/USDT', 'VANRY/USDT', 'ONT/USDT', 'ENJ/USDT', 'ANKR/USDT', 'QKC/USDT', 'MAGIC/USDT', 'COTI/USDT', 'AVA/USDT', 'HMSTR/USDT', 'ZEC/USDT', 'DYM/USDT', 'FXS/USDT', 'METIS/USDT', 'SKL/USDT', 'UTK/USDT', 'GAS/USDT', 'OMNI/USDT', 'QTUM/USDT', 'LRC/USDT', 'KSM/USDT', 'YGG/USDT', 'ACH/USDT', 'GMX/USDT', 'DENT/USDT', 'GLMR/USDT', 'CYBER/USDT', 'POLYX/USDT', 'ACE/USDT', 'TRU/USDT', 'CVX/USDT', 'WIN/USDT', 'JST/USDT', 'HIGH/USDT', 'C98/USDT', 'MBL/USDT', 'REZ/USDT', 'RVN/USDT', 'STORJ/USDT', 'BAT/USDT', 'CATI/USDT', 'CLV/USDT', 'DEGO/USDT', 'XEC/USDT', 'TLM/USDT', 'ID/USDT', 'TNSR/USDT', 'SLP/USDT', 'SXP/USDT', 'ILV/USDT', 'ORCA/USDT', 'FLUX/USDT', 'TFUEL/USDT', 'KAVA/USDT', 'POND/USDT', 'MOVR/USDT', 'MASK/USDT', 'PAXG/USDT', 'BICO/USDT', 'USTC/USDT', 'CHR/USDT', 'ELF/USDT', 'IOTX/USDT', 'API3/USDT', 'NTRN/USDT', 'ICX/USDT', 'HIFI/USDT', 'TWT/USDT', 'DGB/USDT', 'STRAX/USDT', 'OSMO/USDT', 'ALPHA/USDT', 'CVC/USDT', 'NMR/USDT', 'NFP/USDT', 'OGN/USDT', 'SCRT/USDT', 'CELR/USDT', 'RDNT/USDT', 'LSK/USDT', 'UMA/USDT', 'AUCTION/USDT', 'AUDIO/USDT', 'BANANA/USDT', 'ARPA/USDT', 'COMBO/USDT', 'SYN/USDT', 'REQ/USDT', 'SLF/USDT', 'RPL/USDT', 'DUSK/USDT', 'HFT/USDT', 'ALICE/USDT', 'RLC/USDT', 'SUN/USDT', 'GLM/USDT', 'KNC/USDT', 'WAXP/USDT', 'AMB/USDT', 'MAV/USDT', 'G/USDT', 'CTSI/USDT', 'LINA/USDT', 'VIDT/USDT', 'OXT/USDT', 'T/USDT', 'DODO/USDT', 'BAND/USDT', 'MTL/USDT', 'LIT/USDT', 'ADX/USDT', 'VOXEL/USDT', 'PUNDIX/USDT', 'TUSD/USDT', 'AERGO/USDT', 'ALPINE/USDT', 'DIA/USDT', 'ERN/USDT', 'BURGER/USDT', 'PERP/USDT', 'NKN/USDT', 'QI/USDT', 'CREAM/USDT', 'SYS/USDT', 'GTC/USDT', 'BSW/USDT', 'XNO/USDT', 'HARD/USDT', 'DCR/USDT', 'LTO/USDT', 'SFP/USDT', 'USDP/USDT', 'FORTH/USDT', 'GNS/USDT', 'DATA/USDT', 'QUICK/USDT', 'KMD/USDT', 'WAN/USDT', 'LOKA/USDT', 'XEM/USDT', 'WAVES/USDT', 'ETHUP/USDT', 'BTCUP/USDT', 'OMG/USDT', 'XMR/USDT', 'HNT/USDT', 'BULL/USDT', 'EPX/USDT', 'POLS/USDT', 'UNFI/USDT', 'BOND/USDT', 'REN/USDT', 'BSV/USDT', 'BTT/USDT', 'REEF/USDT', 'LOOM/USDT', 'KEY/USDT']

# 🔹 دیکشنری برای ذخیره نتایج
results = {"گروه اول": [], "گروه دوم": [], "گروه سوم": []}

# 🔹 تابع دریافت درصد تغییر در تایم‌فریم‌های مختلف
def get_price_change(symbol, timeframe, periods_ago):
    try:
        now_price = exchange.fetch_ticker(symbol)['last']
        candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=periods_ago + 1)
        if len(candles) < periods_ago + 1:
            return None
        past_price = candles[0][1]
        return ((now_price - past_price) / past_price) * 100
    except Exception as e:
        print(f"خطا در دریافت داده {symbol} با تایم‌فریم {timeframe}: {e}")
        return None

# 🔹 تابع جایگزین برای تغییر 12 ساعته
def get_12h_change(symbol):
    change_12h = get_price_change(symbol, "12h", 1)
    
    if change_12h is None:
        change_6h_1 = get_price_change(symbol, "6h", 1)
        change_6h_2 = get_price_change(symbol, "6h", 2)
        
        if change_6h_1 is not None and change_6h_2 is not None:
            change_12h = change_6h_1 + change_6h_2
    
    if change_12h is None:
        changes_3h = [get_price_change(symbol, "3h", i) for i in range(1, 5)]
        if None not in changes_3h:
            change_12h = sum(changes_3h)

    return change_12h

# 🔹 بررسی شرایط برای هر ارز
for symbol in symbols:
    change_14d = get_price_change(symbol, "1d", 14)
    change_7d = get_price_change(symbol, "1d", 7)
    change_3d = get_price_change(symbol, "1d", 3)
    change_1d = get_price_change(symbol, "1d", 1)
    change_12h = get_12h_change(symbol)

    if change_14d is not None and change_12h is not None and change_14d >= 8 and change_12h <= -4:
        results["گروه اول"].append(symbol)

    if change_7d is not None and change_12h is not None and change_7d >= 6 and change_12h <= -3:
        results["گروه دوم"].append(symbol)

    if change_1d is not None and change_12h is not None and change_1d >= 5 and change_12h <= -3:
        results["گروه سوم"].append(symbol)

# 🔹 آماده‌سازی خروجی نتایج
output_text = ""
for group, coins in results.items():
    output_text += f"{group}\n"
    for coin in coins:
        output_text += f"{coin}\n"
    output_text += "\n"

print(output_text)

# 🔹 تابع برای رسم نمودار
def plot_chart(exchange, symbol, timeframe, length):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        df_length = df.tail(length)
        os.makedirs('charts', exist_ok=True)
        chart_file = f'charts/{symbol.replace("/", "_")}_{timeframe}_{length}candles.png'

        mpf.plot(df_length, type='candle', volume=True, style='yahoo',
                 savefig=dict(fname=chart_file, dpi=100, bbox_inches="tight"))
        return chart_file

    except Exception as e:
        print(f"❌ خطا در رسم نمودار {symbol}: {e}")
        return None

# 🔹 رسم نمودار فقط برای ارزهای انتخاب‌شده در گروه‌ها
chart_files = {"گروه اول": [], "گروه دوم": [], "گروه سوم": []}
for group, coins in results.items():
    for symbol in coins:
        chart = plot_chart(exchange, symbol, "4h", 100)
        if chart:
            chart_files[group].append(chart)

# 🔹 ارسال ایمیل با نمودارهای مربوط به هر گروه
def send_email(subject, body, attachments_by_group):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        for group, files in attachments_by_group.items():
            for file in files:
                with open(file, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
                    msg.attach(part)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("✅ ایمیل با موفقیت ارسال شد!")
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل: {e}")

# 🔹 ارسال ایمیل با نمودارهای مربوط به گروه‌ها
send_email("📊 نتایج تحلیل ارزها + نمودارها", output_text, chart_files)

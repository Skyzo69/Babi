import asyncio
from playwright.async_api import async_playwright
import os

# Fungsi untuk membaca token dari file
def load_tokens(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Gagal membaca file {filename}: {e}")
        return []

discord_tokens = load_tokens("discord_tokens.txt")
twitter_cookies = load_tokens("twitter_cookies.txt")

if not discord_tokens or not twitter_cookies:
    print("Tidak ada token Discord atau cookie Twitter yang ditemukan.")
    exit(1)

channel_id = "1324498333758390353"  # Ganti dengan ID channel yang benar

async def main():
    async with async_playwright() as p:
        # Start the browser in headless mode or with GUI if XServer is available
        browser = await p.chromium.launch(
            headless=true,  # Ganti ke True jika tidak ingin menggunakan GUI
            executable_path="/usr/bin/chromium-browser",  # Pastikan path benar
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        for index, token in enumerate(discord_tokens):
            page = await browser.new_page()
            try:
                print(f"({index + 1}/{len(discord_tokens)}) Login dengan token Discord: {token}")

                # 1. Login ke Discord
                await page.goto("https://discord.com/login", wait_until="networkidle")
                await page.evaluate(f'window.localStorage.setItem("token", "{token}")')
                await page.reload(wait_until="networkidle")

                # 2. Koneksi ke Drip
                print("Login ke app.drip.re...")
                await page.goto("https://app.drip.re/settings?tab=connections", wait_until="networkidle")

                # Klik tombol Connect Discord jika tersedia
                connect_discord_button = await page.query_selector('button:text("Connect Discord")')
                if connect_discord_button:
                    print("Klik tombol Connect Discord...")
                    await connect_discord_button.click()
                    await page.wait_for_navigation(wait_until="networkidle")

                # 3. Set cookies untuk login ke Twitter
                if index < len(twitter_cookies):
                    cookies = [cookie.split("=") for cookie in twitter_cookies[index].split(";")]
                    cookies_dict = [{"name": cookie[0].strip(), "value": cookie[1].strip(), "domain": "twitter.com", "path": "/"} for cookie in cookies]
                    await page.context.add_cookies(cookies_dict)
                    await page.goto("https://twitter.com", wait_until="networkidle")
                    await page.wait_for_selector('div[data-testid="primaryColumn"]', timeout=10000)
                    print("Login berhasil dengan Twitter!")

                # 4. Akses channel Discord dan tekan tombol Verify
                print(f"Mengakses channel ID: {channel_id}")
                await page.goto(f"https://discord.com/channels/@me/{channel_id}", wait_until="networkidle")

                # Pastikan tombol Verify ada sebelum klik
                verify_button = await page.query_selector('button:text("Verify")')
                if verify_button:
                    print("Klik tombol Verify...")
                    await verify_button.click()

                # 5. Kembali ke app.drip.re untuk Unconnect Twitter
                print("Kembali ke app.drip.re untuk Unconnect Twitter...")
                await page.goto("https://app.drip.re/settings?tab=connections", wait_until="networkidle")
                unconnect_twitter_button = await page.query_selector('button:text("Unconnect Twitter")')
                if unconnect_twitter_button:
                    print("Klik tombol Unconnect Twitter...")
                    await unconnect_twitter_button.click()

                # Testing sederhana: Buka halaman lain untuk memastikan Playwright berjalan
                print("Memulai tes halaman...")
                test_page = await browser.new_page()
                await test_page.goto("https://example.com", wait_until="networkidle")
                print("Halaman Example dimuat, Judul:", await test_page.title())
                await test_page.close()

            except Exception as e:
                print(f"Terjadi kesalahan dengan token Discord ({index + 1}): {token}", e)
            finally:
                await page.close()

        print("Semua token selesai diproses. Skrip dihentikan.")
        await browser.close()

# Jalankan fungsi utama
asyncio.run(main())

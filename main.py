from playwright.async_api import async_playwright
import asyncio
import os # Import os module to handle file paths

async def run():
    async with (async_playwright() as playwright):
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # ✅ Open the login page
        await page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        await page.wait_for_load_state('networkidle') # Wait for network to be idle

        # ✅ Fill in username and password
        await page.locator('input[placeholder="Username"]').type("Admin", delay=200)
        await page.locator('input[placeholder="Password"]').type("admin123", delay=200)

        # ✅ Click login
        await page.locator("button[type='submit']").click()

        try:
            # Wait for the Dashboard text to be visible
            await page.wait_for_selector("h6.oxd-text--h6", state='visible', timeout=5000)
            dashboard_text = await page.text_content("h6.oxd-text--h6")
            if dashboard_text.strip() == "Dashboard":
                print("✅ Passed: Login Successful!.")
            else:
                print("❌ Login may have failed. Unexpected text found:", dashboard_text)
        except Exception as e:
            print("❌ Failed: Login Unsuccessful:", e)
            await browser.close()

        # Click on the PIM Menu Icon
        pim_menu = page.locator('//span[@class="oxd-text oxd-text--span oxd-main-menu-item--name" and text()="PIM"]')
        await pim_menu.wait_for(state='visible')
        await pim_menu.click()
        await page.wait_for_load_state('networkidle')

        # Click on the Add button
        add_btn = page.locator('button.oxd-button--secondary:has-text("Add")')
        await add_btn.wait_for(state='visible')
        await add_btn.click()
        await page.wait_for_load_state('networkidle')

        # Fill First Name
        first_name =  page.locator('input.oxd-input[placeholder="First Name"]')
        await first_name.type("Vikram", delay=200)

        # Fill Middle Name
        middle_name = page.locator('input.oxd-input[placeholder="Middle Name"]')
        await middle_name.type("Sharma", delay=200)

        # Fill Last Name
        last_name = page.locator('input.oxd-input[placeholder="Last Name"]')
        await last_name.type("Pottur", delay=200)

        # Enter Employee Code
        emp_code = page.locator("//input[contains(@class, 'oxd-input--active')]").nth(3)
        await emp_code.fill("0225")

        # Enable toggle
        toggle = page.locator("//span[contains(@class, 'oxd-switch-input')]")
        await toggle.wait_for(state='visible') # Ensure the toggle is visible before clicking
        await toggle.click()

        # Enter Username
        username_inputs = page.locator(
            "//input[contains(@class, 'oxd-input') and contains(@class, 'oxd-input--active')]").nth(5)
        await username_inputs.fill("HyderabadCity")

        # Enter the Password
        password = page.locator("//input[@type='password' and contains(@class, 'oxd-input')]").nth(0)
        await password.type("YourPassword123", delay=200)

        # Enter the Confirm Password
        confirm_password = page.locator("//input[@type='password' and contains(@class, 'oxd-input')]").nth(1)
        await confirm_password.type("YourPassword123", delay=200)

        # Upload image
        upload_img_path = 'profile_pic.jpg'
        # Verify the file exists
        if not os.path.exists(upload_img_path):
            print(f"❌ Error: Image file not found at {upload_img_path}")
            await browser.close()
            return # Exit if file not found

        upload_button = page.locator(
            "//button[@type='button' and contains(@class, 'oxd-icon-button--solid-main') and .//i[contains(@class, 'bi-plus')]]")
        await upload_button.wait_for(state='visible') # Wait for the upload button to be visible
        await upload_button.click()

        file_input = await page.wait_for_selector("//input[@type='file']", state="attached")
        await file_input.set_input_files(upload_img_path)
        print(f"✅ Uploaded image: {upload_img_path}")
        await page.wait_for_timeout(1000)

        #Click on the Save Button
        save_button = page.locator("//button[contains(@class, 'oxd-button') and contains(., 'Save')]")
        await save_button.click()
        await page.wait_for_timeout(1000)
    await browser.close()

# ✅ Run the async function
asyncio.run(run())
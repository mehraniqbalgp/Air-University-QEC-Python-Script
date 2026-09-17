import argparse
import os
import shutil
import time
import sys

# Playwright 1.60 does not yet ship ubuntu26.04 browser builds; use 24.04 binaries.
if not os.environ.get("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE") and os.path.isfile("/etc/os-release"):
    with open("/etc/os-release", encoding="utf-8") as f:
        if 'VERSION_ID="26.04"' in f.read():
            os.environ["PLAYWRIGHT_HOST_PLATFORM_OVERRIDE"] = "ubuntu24.04-x64"

from playwright.sync_api import sync_playwright


def launch_browser(playwright):
    """Prefer system Chrome; fall back to Playwright-managed Chromium."""
    launch_kwargs = {"headless": True, "slow_mo": 50}
    if shutil.which("google-chrome") or shutil.which("google-chrome-stable"):
        try:
            return playwright.chromium.launch(channel="chrome", **launch_kwargs)
        except Exception:
            pass
    return playwright.chromium.launch(**launch_kwargs)


def run_qec_automation(username, password):
    with sync_playwright() as p:
        browser = launch_browser(p)
        context = browser.new_context()
        page = context.new_page()

        # Handle alerts (ASP.NET often uses them)
        page.on("dialog", lambda dialog: dialog.accept())

        # 1. LOGIN
        print(f"Logging in user {username}...")
        page.goto("https://portals.au.edu.pk/QEC/login.aspx")
        page.select_option("#ctl00_ContentPlaceHolder2_ddlcampus", value="Islamabad")
        page.select_option("#ctl00_ContentPlaceHolder2_ddlUserType", value="Student/Alumni")
        page.fill("#ctl00_ContentPlaceHolder2_txt_regid", username)
        page.fill("#ctl00_ContentPlaceHolder2_txt_password", password)
        page.click("#ctl00_ContentPlaceHolder2_btnAccountlogin")
        page.wait_for_load_state("networkidle")
        
        # Simple check if login failed (e.g. invalid credentials)
        if page.locator("#ctl00_ContentPlaceHolder2_txt_regid").count() > 0:
             print("Login failed! Please check your credentials.")
             browser.close()
             sys.exit(1)
             
        print("Login successful.")

        # --- SECTION: Student Course Evaluation ---
        fill_course_eval(page)

        # --- SECTION: Teacher Evaluation ---
        fill_teacher_eval(page)

        # --- SECTION: Online Learning Feedback ---
        fill_online_learning(page)

        print("\nAll tasks completed!")
        browser.close()

def fill_course_eval(page):
    print("\nStarting: Student Course Evaluation")
    page.goto("https://portals.au.edu.pk/QEC/p1.aspx")
    
    while True:
        # Get course options
        options = page.eval_on_selector("#ctl00_ContentPlaceHolder2_cmb_courses", 
            "select => Array.from(select.options).map(o => ({text: o.text, value: o.value}))")
        
        # Filter out "---Select---"
        to_eval = [o for o in options if o["value"] != "0" and "---" not in o["text"]]
        
        if not to_eval:
            print("No more courses left for evaluation.")
            break
            
        target = to_eval[0]
        print(f"Evaluating Course: {target['text']}")
        
        # Select course which triggers PostBack
        page.select_option("#ctl00_ContentPlaceHolder2_cmb_courses", value=target["value"])
        page.wait_for_load_state("networkidle")
        time.sleep(2) # Extra buffer for ASP.NET

        # Fill questions (1-12)
        for i in range(1, 13):
            selector = f"#ctl00_ContentPlaceHolder2_q{i}_1"
            if page.locator(selector).count() > 0:
                page.click(selector)
        
        # Submit
        page.click("#ctl00_ContentPlaceHolder2_btnSave")
        page.wait_for_load_state("networkidle")
        print(f"Submitted: {target['text']}")
        time.sleep(2)

def fill_teacher_eval(page):
    print("\nStarting: Teacher Evaluation")
    page.goto("https://portals.au.edu.pk/QEC/p10.aspx")
    
    while True:
        # Teacher Dropdown
        teachers = page.eval_on_selector("#ctl00_ContentPlaceHolder2_ddlTeacher", 
            "select => Array.from(select.options).map(o => ({text: o.text, value: o.value}))")
        
        to_eval_teacher = [t for t in teachers if t["value"] != "0" and "---" not in t["text"]]
        
        if not to_eval_teacher:
            print("No more teachers left for evaluation.")
            break
            
        t_target = to_eval_teacher[0]
        print(f"Evaluating Teacher: {t_target['text']}")
        
        # Select Teacher
        page.select_option("#ctl00_ContentPlaceHolder2_ddlTeacher", value=t_target["value"])
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Now check course dropdown (sometimes there's only one, sometimes multiple)
        courses = page.eval_on_selector("#ctl00_ContentPlaceHolder2_ddlCourse", 
            "select => Array.from(select.options).map(o => ({text: o.text, value: o.value}))")
        
        to_eval_course = [c for c in courses if c["value"] != "0" and "---" not in c["text"]]
        
        if not to_eval_course:
            # Maybe it reloaded and teacher disappeared? Or no courses?
            print("No courses found for this teacher.")
            break

        print(f"  Course: {to_eval_course[0]['text']}")
        page.select_option("#ctl00_ContentPlaceHolder2_ddlCourse", value=to_eval_course[0]["value"])
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Fill questions (1-16)
        for i in range(1, 17):
            selector = f"#ctl00_ContentPlaceHolder2_q{i}_1"
            if page.locator(selector).count() > 0:
                page.click(selector)
        
        # Comments (q20, q21)
        if page.locator("#ctl00_ContentPlaceHolder2_q20").count() > 0:
            page.fill("#ctl00_ContentPlaceHolder2_q20", "Good")
        if page.locator("#ctl00_ContentPlaceHolder2_q21").count() > 0:
            page.fill("#ctl00_ContentPlaceHolder2_q21", "Excellent")

        # Submit
        page.click("#ctl00_ContentPlaceHolder2_btnSave")
        page.wait_for_load_state("networkidle")
        print(f"Submitted Teacher Eval for: {t_target['text']}")
        time.sleep(2)

def fill_online_learning(page):
    print("\nStarting: Online Learning Feedback")
    page.goto("https://portals.au.edu.pk/QEC/p10a_learning_online_form.aspx")
    
    while True:
        # Course Dropdown (Note ContentPlaceHolder1)
        options = page.eval_on_selector("#ctl00_ContentPlaceHolder1_cmb_courses", 
            "select => Array.from(select.options).map(o => ({text: o.text, value: o.value}))")
        
        to_eval = [o for o in options if o["value"] != "0" and "---" not in o["text"]]
        
        if not to_eval:
            print("No more online learning feedback forms left.")
            break
            
        target = to_eval[0]
        print(f"Evaluating Online: {target['text']}")
        
        page.select_option("#ctl00_ContentPlaceHolder1_cmb_courses", value=target["value"])
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Questions (1-15)
        for i in range(1, 16):
            selector = f"#ctl00_ContentPlaceHolder1_q{i}_1"
            if page.locator(selector).count() > 0:
                page.click(selector)
        
        # Comment (q20)
        if page.locator("#ctl00_ContentPlaceHolder1_q20").count() > 0:
            page.fill("#ctl00_ContentPlaceHolder1_q20", "N/A")

        # Submit
        page.click("#ctl00_ContentPlaceHolder1_btnSave")
        page.wait_for_load_state("networkidle")
        print(f"Submitted Online Feedback for: {target['text']}")
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QEC Automation Script")
    parser.add_argument("--username", required=True, help="Portal Registration ID")
    parser.add_argument("--password", required=True, help="Portal Password")
    args = parser.parse_args()
    
    run_qec_automation(args.username, args.password)


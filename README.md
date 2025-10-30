
---

# Klgr: Keylogger with Discord Reporting

## Description

Klgr is a Python-based keylogger that captures keystrokes and sends reports to a specified Discord webhook. The tool is designed for educational purposes and should be used only in environments where you have explicit permission. Unauthorized use of this software is illegal and unethical.

This README provides a step-by-step guide on how to convert the Python script into an executable (EXE) file for easier deployment.

## Table of Contents

1. [Disclaimer](#disclaimer)
2. [Features](#features)
3. [Installation](#installation)
4. [Converting to EXE](#converting-to-exe)
   - [Step 1: Install PyInstaller](#step-1-install-pyinstaller)
   - [Step 2: Modify the Script](#step-2-modify-the-script)
   - [Step 3: Create the EXE](#step-3-create-the-exe)
   - [Step 4: Test the EXE](#step-4-test-the-exe)
5. [Usage](#usage)
6. [Legal Use](#legal-use)
7. [Contributing](#contributing)
8. [License](#license)

## Disclaimer

**Warning:** This software is intended for educational purposes only. Unauthorized use of this software to capture keystrokes or any other data from a system without explicit permission is illegal and unethical. Always obtain clear and explicit consent before using this software on any device or network.

By using this software, you agree to take full responsibility for your actions and to abide by all applicable laws.

## Features

- **Keylogging**: Captures all keystrokes and logs them.
- **Discord Reporting**: Sends logs to a Discord webhook at specified intervals.
- **Startup Persistence**: Optionally sets the program to run at system startup.
- **Command Control**: Allows the operator to send specific commands via Discord to trigger reports.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Klgr.git
   cd Klgr
   ```

2. **Install Dependencies**
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

   Ensure that all dependencies, including `PyInstaller`, `keyboard`, `requests`, `discord-webhook`, and others, are installed.

## Converting to EXE

### Step 1: Install PyInstaller

PyInstaller is a popular tool for converting Python scripts into standalone executables.

```bash
pip install pyinstaller
```

### Step 2: Modify the Script

Before creating the EXE, ensure the script is configured with your Discord webhook URL. Replace `<YOUR_DISCORD_WEBHOOK_URL>` in the script with your actual webhook URL.

Ensure that all paths and settings are correct, especially if you're planning to distribute the executable on different machines.

### Step 3: Create the EXE

Use PyInstaller to convert the script into an executable:

```bash
pyinstaller --onefile --noconsole klgr.py
```

- `--onefile`: Packages everything into a single executable.
- `--noconsole`: Hides the console window when running the EXE.

This command will generate a `dist` folder containing the `klgr.exe` file.

### Step 4: Test the EXE

1. Navigate to the `dist` folder:
   ```bash
   cd dist
   ```

2. Run the executable to ensure it works as expected:
   ```bash
   ./klgr.exe
   ```

Test the keylogger in a controlled environment to ensure it captures keystrokes and sends them to the Discord webhook correctly.

## Usage

1. **Run the EXE**: Double-click the `klgr.exe` file to start the keylogger. It will run in the background, capturing keystrokes and sending logs to your Discord webhook at the specified intervals.

2. **Control Commands**: You can send the `/log_keys` command to the Discord webhook to trigger a manual report.

3. **Startup Persistence**: The program is configured to set itself up to run on system startup. Ensure this feature is enabled only if necessary.

## Legal Use

This software must only be used in environments where you have explicit permission to monitor keystrokes. Examples of legal use cases include:

- **Testing Security**: Using the tool in penetration testing environments with consent.
- **Parental Monitoring**: With the full knowledge and consent of the user.
- **Corporate Environments**: Where explicit permission has been granted by employees.

**It is illegal and unethical to use this software for unauthorized surveillance or to capture keystrokes from devices without explicit consent.**

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE.md` file for details.

---

**Update Notice:** This README was last updated on **August 23, 2024**, with version **1.1**. The latest update fixed issues with the keylogging functionality that was not working correctly in the previous version 1.0, and added a watermark. 



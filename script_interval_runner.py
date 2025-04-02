import json
import time
import importlib
import os
import logging
import threading
import sys
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

class ScriptConfig:
    def __init__(self, name, filename, method, interval, retry_on_error, launch_flags):
        self.name = name
        self.filename = filename
        self.method = method
        self.interval = interval
        self.retry_on_error = retry_on_error
        self.launch_flags = launch_flags  # This will store the flags
        self.failure_count = 0  # Track the failure count

    def __repr__(self):
        return f"ScriptConfig(name={self.name}, filename={self.filename}, method={self.method}, interval={self.interval}, retry_on_error={self.retry_on_error}, launch_flags={self.launch_flags}, failure_count={self.failure_count})"


class ScriptRunner:
    def __init__(self, config_file):
        self.scripts = []
        self.load_config(config_file)
        # Retrieve the Discord webhook URLs from the environment variables
        self.logs_webhook_url = os.getenv('SCRIPT_LOGS_DISCORD_WEBHOOK_URL')
        self.errors_webhook_url = os.getenv('SCRIPT_ERROR_DISCORD_WEBHOOK_URL')

    def load_config(self, config_file):
        """Load script configurations from a JSON file."""
        if not os.path.exists(config_file):
            logging.error(f"Config file '{config_file}' not found.")
            return

        with open(config_file, 'r') as f:
            data = json.load(f)
            for item in data:
                # Read launch_flags as a list (it could be an empty list if no flags are present)
                launch_flags = item.get('launch_flags', [])

                script_config = ScriptConfig(
                    name=item['name'],
                    filename=item['filename'],
                    method=item['method'],
                    interval=item['interval'],
                    retry_on_error=item['retry_on_error'].lower() == 'true',
                    launch_flags=launch_flags  # Store launch flags
                )
                self.scripts.append(script_config)

    def send_to_discord(self, webhook_url, message):
        """Send a message to a Discord webhook."""
        if webhook_url:
            try:
                payload = {'content': message}
                requests.post(webhook_url, json=payload)
            except Exception as e:
                logging.error(f"Failed to send message to Discord: {e}")

    def run_script(self, script_config):
        """Run the script as per configuration."""
        script_path = os.path.join(os.getcwd(), script_config.filename)

        if not os.path.exists(script_path):
            logging.error(f"Script file '{script_config.filename}' not found in the current directory.")
            return

        try:
            # Import the script as a module
            script_name = script_config.filename[:-3]  # Strip ".py" from the filename
            module = importlib.import_module(script_name)

            # Temporarily modify sys.argv to simulate command-line arguments
            original_argv = sys.argv
            sys.argv = [script_name] + script_config.launch_flags  # Simulate command-line args

            # Check if method exists
            if hasattr(module, script_config.method):
                method = getattr(module, script_config.method)
                retry_count = 0
                while True:
                    try:
                        logging.info(f"Running {script_config.name} with flags: {script_config.launch_flags}...")
                        # Call the method without needing to pass arguments (sys.argv is used)
                        method()
                        # Log successful run to Discord
                        if self.logs_webhook_url:
                            self.send_to_discord(self.logs_webhook_url, f"Successfully ran {script_config.name}")
                        logging.info(f"Completed {script_config.name}.")
                        time.sleep(script_config.interval)  # Sleep after execution before next run
                        script_config.failure_count = 0  # Reset failure count after a successful run
                    except Exception as e:
                        logging.error(f"Error running {script_config.name}: {e}")
                        script_config.failure_count += 1
                        if script_config.failure_count >= 3:  # Notify on third failure
                            error_message = f"{script_config.name} has failed 3 times. Last error: {e}"
                            if self.errors_webhook_url:
                                self.send_to_discord(self.errors_webhook_url, error_message)
                            logging.error(f"Max retry attempts reached for {script_config.name}. Error sent to Discord.")
                            return 500 # return error code
                        if script_config.retry_on_error:
                            retry_count += 1
                            if retry_count >= 3:  # Retry 3 times
                                logging.error(f"Max retry attempts reached for {script_config.name}.")
                                return 500
                            logging.info(f"Retrying {script_config.name}... ({retry_count}/3)")
                        else:
                            break
            else:
                logging.error(f"Method '{script_config.method}' not found in {script_config.filename}")

            # Restore the original sys.argv
            sys.argv = original_argv
        except Exception as e:
            logging.error(f"Failed to run script {script_config.filename}: {e}")
            return 404 # return not found if script not found

        return 200 # return success

    def run_script_in_thread(self, script_config):
        """Run the script in a separate thread with an endless loop."""
        def target():
            error_count = 0
            while error_count < 3:
                error_code = self.run_script(script_config)
                if error_code == 404:
                    error_count += 1
                    time.sleep(5)
                elif error_code == 500:
                    break
                else:
                    error_count = 0 # Reset error count on success

            logging.error(f"Script {script_config.name} has failed 3 times. Stopping execution.")

        thread = threading.Thread(target=target)
        thread.daemon = True  # Allow the thread to exit when the main program exits
        thread.start()
        return thread

    def run_all_scripts(self):
        """Start all scripts concurrently in separate threads with an endless loop."""
        threads = []
        for script_config in self.scripts:
            thread = self.run_script_in_thread(script_config)
            threads.append(thread)

        # The main thread only needs to start the loops, it doesn't need to join since the threads are infinite
        logging.info("All scripts have been started and are running in their respective threads.")

# Main execution
if __name__ == "__main__":
    config_file = 'scripts_config.json'
    runner = ScriptRunner(config_file)
    runner.run_all_scripts()

    # Keep the main program running (this is important for the daemon threads to keep running)
    while True:
        time.sleep(1)

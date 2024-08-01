using System;
using System.Collections.Generic;
using FlaUI.Core.AutomationElements;
using FlaUI.UIA2;

namespace WinAutoGui
{
    public class WinAutoGui
    {
        public void TestMethod()
        {
            // Use UIA2 Automation
            using (var automation = new UIA2Automation())
            {
                // Attach to the current Wawi-process
                var app = FlaUI.Core.Application.Attach("Notepad.exe");

                // Get the main window
                AutomationElement mainWindow = app.GetMainWindow(automation);
                Console.WriteLine("Window title: " + mainWindow.Name);
            }
        }

        public string GetWindowTitle()
        {
            return "Window title";
        }

        public object ReadStatusbar()
        {
            return new Dictionary<string, string>()
            {
                {"status", "INFO"},
                {"message", "OK"}
            };
        }

        public void PushButton(string label)
        {
            // throw new NotImplementedException($"The button '{label}' was not found");
            Console.WriteLine("Done");
        }
    }
}

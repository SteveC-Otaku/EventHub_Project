// Settings page script
document.addEventListener("DOMContentLoaded", () => {
  // Check if user is logged in
  const loggedInUserJson = localStorage.getItem("loggedInUser")
  if (!loggedInUserJson) {
    window.location.href = "index.html"
    return
  }

  const loggedInUser = JSON.parse(loggedInUserJson)

  // Get DOM elements
  const settingsForm = document.getElementById("settings-form")
  const resetBtn = document.getElementById("reset-btn")
  const changePasswordBtn = document.getElementById("change-password-btn")
  const twoFactorBtn = document.getElementById("two-factor-btn")
  const deleteAccountBtn = document.getElementById("delete-account-btn")

  // Load user settings
  loadSettings()

  // Event listeners
  settingsForm.addEventListener("submit", (e) => {
    e.preventDefault()
    saveSettings()
  })

  resetBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to reset all settings to default values?")) {
      resetToDefaults()
    }
  })

  changePasswordBtn.addEventListener("click", () => {
    // Simulate password change
    const newPassword = prompt("Enter new password:")
    if (newPassword) {
      alert("Password changed successfully!")
    }
  })

  twoFactorBtn.addEventListener("click", () => {
    // Simulate two-factor authentication setup
    alert("Two-factor authentication setup would be implemented here")
  })

  deleteAccountBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
      if (confirm("This will permanently delete all your data. Are you absolutely sure?")) {
        deleteAccount()
      }
    }
  })

  // Function to load settings
  function loadSettings() {
    // Get user settings from localStorage or use defaults
    const settings = JSON.parse(localStorage.getItem(`userSettings_${loggedInUser.id}`)) || getDefaultSettings()

    // Populate form fields
    document.getElementById("email-notifications").checked = settings.emailNotifications
    document.getElementById("sms-notifications").checked = settings.smsNotifications
    document.getElementById("marketing-emails").checked = settings.marketingEmails
    document.getElementById("profile-public").checked = settings.profilePublic
    document.getElementById("show-attendance").checked = settings.showAttendance
    document.getElementById("language").value = settings.language
    document.getElementById("timezone").value = settings.timezone
    document.getElementById("currency").value = settings.currency
  }

  // Function to get default settings
  function getDefaultSettings() {
    return {
      emailNotifications: true,
      smsNotifications: false,
      marketingEmails: false,
      profilePublic: false,
      showAttendance: false,
      language: "en",
      timezone: "UTC-5",
      currency: "USD",
    }
  }

  // Function to save settings
  function saveSettings() {
    const settings = {
      emailNotifications: document.getElementById("email-notifications").checked,
      smsNotifications: document.getElementById("sms-notifications").checked,
      marketingEmails: document.getElementById("marketing-emails").checked,
      profilePublic: document.getElementById("profile-public").checked,
      showAttendance: document.getElementById("show-attendance").checked,
      language: document.getElementById("language").value,
      timezone: document.getElementById("timezone").value,
      currency: document.getElementById("currency").value,
    }

    // Save settings to localStorage
    localStorage.setItem(`userSettings_${loggedInUser.id}`, JSON.stringify(settings))

    // Show success message
    alert("Settings saved successfully!")
  }

  // Function to reset to defaults
  function resetToDefaults() {
    const defaultSettings = getDefaultSettings()

    // Update form fields
    document.getElementById("email-notifications").checked = defaultSettings.emailNotifications
    document.getElementById("sms-notifications").checked = defaultSettings.smsNotifications
    document.getElementById("marketing-emails").checked = defaultSettings.marketingEmails
    document.getElementById("profile-public").checked = defaultSettings.profilePublic
    document.getElementById("show-attendance").checked = defaultSettings.showAttendance
    document.getElementById("language").value = defaultSettings.language
    document.getElementById("timezone").value = defaultSettings.timezone
    document.getElementById("currency").value = defaultSettings.currency

    // Save default settings
    localStorage.setItem(`userSettings_${loggedInUser.id}`, JSON.stringify(defaultSettings))

    alert("Settings reset to defaults!")
  }

  // Function to delete account
  function deleteAccount() {
    // Remove user data
    localStorage.removeItem("loggedInUser")
    localStorage.removeItem(`userSettings_${loggedInUser.id}`)

    // In a real application, you would also:
    // - Delete user from the database
    // - Cancel all registrations
    // - Remove user from all events

    alert("Account deleted successfully!")
    window.location.href = "index.html"
  }
})

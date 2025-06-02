// Profile page script
document.addEventListener("DOMContentLoaded", () => {
  // Check if user is logged in
  const loggedInUserJson = localStorage.getItem("loggedInUser")
  if (!loggedInUserJson) {
    window.location.href = "index.html"
    return
  }

  const loggedInUser = JSON.parse(loggedInUserJson)

  // Get DOM elements
  const profileForm = document.getElementById("profile-form")
  const userStatusBadge = document.getElementById("user-status-badge")
  const eventsAttendedElement = document.getElementById("events-attended")
  const totalSpentElement = document.getElementById("total-spent")
  const memberSinceElement = document.getElementById("member-since")
  const cancelBtn = document.getElementById("cancel-btn")
  const avatarUploadBtn = document.getElementById("avatar-upload-btn")

  // Load user profile data
  loadProfileData()

  // Event listeners
  profileForm.addEventListener("submit", (e) => {
    e.preventDefault()
    saveProfile()
  })

  cancelBtn.addEventListener("click", () => {
    loadProfileData() // Reset form to original values
  })

  avatarUploadBtn.addEventListener("click", () => {
    // Simulate avatar upload
    alert("Avatar upload functionality would be implemented here")
  })

  // Function to load profile data
  function loadProfileData() {
    // Get user data from the data service
    const user = window.dataService.getUser(loggedInUser.id)

    if (!user) {
      alert("User not found")
      return
    }

    // Populate form fields
    document.getElementById("full-name").value = user.name || ""
    document.getElementById("email").value = user.email || ""
    document.getElementById("phone").value = user.phone || ""
    document.getElementById("bio").value = user.bio || ""
    document.getElementById("location").value = user.location || ""

    // Set interests checkboxes
    if (user.interests) {
      user.interests.forEach((interest) => {
        const checkbox = document.querySelector(`input[name="interests"][value="${interest}"]`)
        if (checkbox) {
          checkbox.checked = true
        }
      })
    }

    // Update status badge
    if (user.isVIP) {
      userStatusBadge.textContent = "VIP User"
      userStatusBadge.className = "profile__status-badge profile__status-badge--vip"
    } else {
      userStatusBadge.textContent = "Regular User"
      userStatusBadge.className = "profile__status-badge profile__status-badge--regular"
    }

    // Calculate and display statistics
    calculateStatistics(user)
  }

  // Function to calculate user statistics
  function calculateStatistics(user) {
    // Get user's registrations
    const registrations = window.dataService.getRegistrationsByUser(user.id)

    // Calculate events attended (past events)
    const currentDate = new Date()
    let eventsAttended = 0
    let totalSpent = 0

    registrations.forEach((registration) => {
      const event = window.dataService.getEvent(registration.eventId)
      if (event) {
        const eventDate = new Date(event.date + "T" + event.time)
        if (eventDate < currentDate) {
          eventsAttended++
        }
        totalSpent += registration.totalPrice
      }
    })

    // Update statistics display
    eventsAttendedElement.textContent = eventsAttended
    totalSpentElement.textContent = `$${totalSpent.toFixed(2)}`

    // For member since, we'll use a default year or calculate from first registration
    const memberSince =
      registrations.length > 0 ? new Date(registrations[0].purchaseDate).getFullYear() : new Date().getFullYear()
    memberSinceElement.textContent = memberSince
  }

  // Function to save profile
  function saveProfile() {
    // Get form data
    const formData = new FormData(profileForm)

    // Get selected interests
    const interests = []
    document.querySelectorAll('input[name="interests"]:checked').forEach((checkbox) => {
      interests.push(checkbox.value)
    })

    // Update user object
    const updatedUser = {
      ...loggedInUser,
      name: formData.get("fullName"),
      email: formData.get("email"),
      phone: formData.get("phone"),
      bio: formData.get("bio"),
      location: formData.get("location"),
      interests: interests,
    }

    // Save to data service
    window.dataService.saveUser(updatedUser)

    // Update logged in user in localStorage
    localStorage.setItem("loggedInUser", JSON.stringify(updatedUser))

    // Show success message
    alert("Profile updated successfully!")

    // Reload the page to reflect changes
    window.location.reload()
  }
})

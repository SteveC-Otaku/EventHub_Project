// Organizer Login page script
document.addEventListener("DOMContentLoaded", () => {
  // Get DOM elements
  const loginForm = document.getElementById("login-form")
  const emailInput = document.getElementById("email")
  const passwordInput = document.getElementById("password")
  const loginError = document.getElementById("login-error")

  // Demo organizer buttons
  const demoTechOrganizer = document.getElementById("demo-tech-organizer")
  const demoMusicOrganizer = document.getElementById("demo-music-organizer")
  const demoBusinessOrganizer = document.getElementById("demo-business-organizer")

  // Demo organizer event listeners
  if (demoTechOrganizer) {
    demoTechOrganizer.addEventListener("click", () => {
      loginDemoOrganizer("tech@demo.com", "Tech Events Inc.")
    })
  }

  if (demoMusicOrganizer) {
    demoMusicOrganizer.addEventListener("click", () => {
      loginDemoOrganizer("music@demo.com", "Music Festivals LLC")
    })
  }

  if (demoBusinessOrganizer) {
    demoBusinessOrganizer.addEventListener("click", () => {
      loginDemoOrganizer("business@demo.com", "Business Network Association")
    })
  }

  // Event listener for form submission
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Get input values
    const email = emailInput.value.trim() || "organizer@example.com"
    const password = passwordInput.value || "password"

    // Accept any credentials - fake login
    fakeLogin(email)
  })

  // Function to login demo organizer
  function loginDemoOrganizer(email, organizationName) {
    // Check if an organizer with this email exists
    let organizer = window.dataService.getOrganizerByEmail(email)

    // If not, create a new organizer with predefined data
    if (!organizer) {
      organizer = {
        name: organizationName,
        email: email,
        password: "password123", // In a real app, this would be hashed
        events: [],
      }
      organizer = window.dataService.saveOrganizer(organizer)
    }

    // Store organizer ID in sessionStorage
    sessionStorage.setItem("organizerId", organizer.id)

    // Redirect to organizer dashboard
    window.location.href = "organizer-dashboard.html"
  }

  // Function for fake login
  function fakeLogin(email) {
    // Check if an organizer with this email exists
    let organizer = window.dataService.getOrganizerByEmail(email)

    // If not, create a new organizer
    if (!organizer) {
      organizer = {
        name: email.split("@")[0] + "'s Organization",
        email: email,
        password: "password123", // In a real app, this would be hashed
        events: [],
      }
      organizer = window.dataService.saveOrganizer(organizer)
    }

    // Store organizer ID in sessionStorage
    sessionStorage.setItem("organizerId", organizer.id)

    // Redirect to organizer dashboard
    window.location.href = "organizer-dashboard.html"
  }
})

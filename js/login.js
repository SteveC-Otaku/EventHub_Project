// Login functionality
document.addEventListener("DOMContentLoaded", () => {
  // Get DOM elements
  const loginContainer = document.getElementById("login-container")
  const loginButton = document.getElementById("login-button")
  const loginModal = document.getElementById("login-modal")
  const loginForm = document.getElementById("login-modal-form")
  const modalClose = loginModal.querySelector(".modal__close")

  // Demo account buttons
  const demoRegularUser = document.getElementById("demo-regular-user")
  const demoVipUser = document.getElementById("demo-vip-user")

  // Check if user is already logged in
  checkLoginStatus()

  // Event listeners
  if (loginButton) {
    loginButton.addEventListener("click", (e) => {
      e.preventDefault()
      loginModal.classList.add("active")
    })
  }

  if (modalClose) {
    modalClose.addEventListener("click", () => {
      loginModal.classList.remove("active")
    })
  }

  // Demo account event listeners
  if (demoRegularUser) {
    demoRegularUser.addEventListener("click", () => {
      loginDemoUser("john.doe@demo.com", false)
      loginModal.classList.remove("active")
    })
  }

  if (demoVipUser) {
    demoVipUser.addEventListener("click", () => {
      loginDemoUser("jane.vip@demo.com", true)
      loginModal.classList.remove("active")
    })
  }

  // Close modal when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target === loginModal) {
      loginModal.classList.remove("active")
    }
  })

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Get form data
      const email = document.getElementById("login-email").value.trim() || "user@example.com"
      const password = document.getElementById("login-password").value || "password"

      // Fake login - accept any credentials
      loginUser(email)

      // Close modal
      loginModal.classList.remove("active")
    })
  }

  // Function to check login status
  function checkLoginStatus() {
    const loggedInUser = localStorage.getItem("loggedInUser")

    if (loggedInUser) {
      // User is logged in
      displayUserProfile(JSON.parse(loggedInUser))
    }
  }

  // Function to login demo user
  function loginDemoUser(email, isVIP) {
    // Check if user exists in the system
    let user = window.dataService.getUserByEmail(email)

    // If user doesn't exist, create a new one with predefined data
    if (!user) {
      const userName = isVIP ? "Jane Smith (VIP)" : "John Doe"
      user = window.dataService.saveUser({
        name: userName,
        email: email,
        registrations: [],
        isVIP: isVIP,
        phone: isVIP ? "+1 (555) 987-6543" : "+1 (555) 123-4567",
        bio: isVIP
          ? "VIP member who loves exclusive events and premium experiences."
          : "Regular user who enjoys attending various events and meeting new people.",
        location: isVIP ? "San Francisco, CA" : "New York, NY",
        interests: isVIP ? ["conferences", "networking"] : ["workshops", "concerts"],
      })
    }

    // Store logged in user in localStorage
    localStorage.setItem("loggedInUser", JSON.stringify(user))

    // Update UI
    displayUserProfile(user)
  }

  // Function to login user
  function loginUser(email) {
    // Check if user exists in the system
    let user = window.dataService.getUserByEmail(email)

    // If user doesn't exist, create a new one
    if (!user) {
      user = window.dataService.saveUser({
        name: email.split("@")[0], // Use part of email as name
        email: email,
        registrations: [],
        isVIP: Math.random() > 0.5, // Randomly assign VIP status
      })
    }

    // Store logged in user in localStorage
    localStorage.setItem("loggedInUser", JSON.stringify(user))

    // Update UI
    displayUserProfile(user)
  }

  // Function to display user profile
  function displayUserProfile(user) {
    if (!loginContainer) return

    // Create user profile HTML
    loginContainer.innerHTML = `
          <div class="user-profile">
              <img src="/placeholder.svg?height=32&width=32" alt="User Avatar" class="user-avatar">
              <span class="user-profile__name">${user.name}</span>
              ${
                user.isVIP
                  ? '<span class="user-profile__badge user-profile__badge--vip">VIP</span>'
                  : '<span class="user-profile__badge user-profile__badge--regular">User</span>'
              }
              <div class="user-profile__dropdown">
                  <div class="user-profile__dropdown-item"><a href="profile.html">Profile</a></div>
                  <div class="user-profile__dropdown-item"><a href="settings.html">Settings</a></div>
                  <div class="user-profile__dropdown-item" id="logout-button">Logout</div>
              </div>
          </div>
      `

    // Add event listener to toggle dropdown
    const userProfile = loginContainer.querySelector(".user-profile")
    const dropdown = loginContainer.querySelector(".user-profile__dropdown")

    userProfile.addEventListener("click", (e) => {
      dropdown.classList.toggle("active")
      e.stopPropagation()
    })

    // Close dropdown when clicking outside
    document.addEventListener("click", () => {
      dropdown.classList.remove("active")
    })

    // Add event listener to logout button
    const logoutButton = document.getElementById("logout-button")
    if (logoutButton) {
      logoutButton.addEventListener("click", () => {
        localStorage.removeItem("loggedInUser")
        window.location.reload()
      })
    }
  }
})

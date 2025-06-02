// Organizer Create Event page script
document.addEventListener("DOMContentLoaded", () => {
  // Get DOM elements
  const createEventForm = document.getElementById("create-event-form")
  const cancelButton = document.getElementById("cancel-button")

  // Get organizer ID from session storage
  const organizerId = sessionStorage.getItem("organizerId")

  // Check if organizer is logged in
  if (!organizerId) {
    window.location.href = "organizer-login.html"
    return
  }

  // Check if we're editing an existing event
  const editEventId = sessionStorage.getItem("editEventId")
  let isEditing = false
  let currentEvent = null

  if (editEventId) {
    isEditing = true
    currentEvent = window.dataService.getEvent(Number.parseInt(editEventId))

    if (currentEvent) {
      // Populate form with event data
      populateForm(currentEvent)
      // Update page title
      document.querySelector(".create-event__title").textContent = "Edit Event"
    }
  }

  // Event listeners
  cancelButton.addEventListener("click", () => {
    // Clear edit event ID if it exists
    sessionStorage.removeItem("editEventId")

    // Go back to events page
    window.location.href = "organizer-events.html"
  })

  createEventForm.addEventListener("submit", (e) => {
    e.preventDefault()

    // Get form data
    const formData = new FormData(createEventForm)

    // Validate form
    if (!validateForm(formData)) {
      return
    }

    // Create or update event
    if (isEditing) {
      updateEvent(formData)
    } else {
      createEvent(formData)
    }
  })

  // Function to populate form for editing
  function populateForm(event) {
    document.getElementById("event-name").value = event.title
    document.getElementById("event-category").value = event.category
    document.getElementById("event-description").value = event.description
    document.getElementById("event-date").value = event.date
    document.getElementById("event-time").value = event.time
    document.getElementById("event-location").value = event.location
    document.getElementById("general-price").value = event.tickets.general.price
    document.getElementById("general-capacity").value = event.tickets.general.capacity
    document.getElementById("vip-price").value = event.tickets.vip.price
    document.getElementById("vip-capacity").value = event.tickets.vip.capacity
  }

  // Function to validate form
  function validateForm(formData) {
    const eventName = formData.get("eventName")
    const eventDate = formData.get("eventDate")
    const generalPrice = formData.get("generalPrice")
    const generalCapacity = formData.get("generalCapacity")

    if (!eventName || !eventDate || !generalPrice || !generalCapacity) {
      alert("Please fill in all required fields.")
      return false
    }

    // Check if event date is in the future
    const selectedDate = new Date(eventDate)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    if (selectedDate < today) {
      alert("Event date must be in the future.")
      return false
    }

    // Check if prices are valid
    if (Number.parseFloat(generalPrice) < 0 || Number.parseFloat(formData.get("vipPrice")) < 0) {
      alert("Prices cannot be negative.")
      return false
    }

    // Check if capacities are valid
    if (Number.parseInt(generalCapacity) <= 0 || Number.parseInt(formData.get("vipCapacity")) < 0) {
      alert("Capacities must be positive numbers.")
      return false
    }

    return true
  }

  // Function to create new event
  function createEvent(formData) {
    // Get organizer data
    const organizer = window.dataService.getOrganizer(Number.parseInt(organizerId))

    if (!organizer) {
      alert("Organizer not found. Please log in again.")
      return
    }

    // Create event object
    const event = {
      title: formData.get("eventName"),
      description: formData.get("eventDescription"),
      date: formData.get("eventDate"),
      time: formData.get("eventTime"),
      location: formData.get("eventLocation"),
      category: formData.get("eventCategory"),
      image: "/placeholder.svg?height=300&width=500", // Default image
      organizer: {
        id: organizer.id,
        name: organizer.name,
        email: organizer.email,
      },
      tickets: {
        general: {
          price: Number.parseFloat(formData.get("generalPrice")),
          capacity: Number.parseInt(formData.get("generalCapacity")),
          remaining: Number.parseInt(formData.get("generalCapacity")),
        },
        vip: {
          price: Number.parseFloat(formData.get("vipPrice")),
          capacity: Number.parseInt(formData.get("vipCapacity")),
          remaining: Number.parseInt(formData.get("vipCapacity")),
        },
      },
      attendees: [],
    }

    // Save event
    const savedEvent = window.dataService.saveEvent(event)

    // Update organizer's events list
    if (!organizer.events) {
      organizer.events = []
    }
    organizer.events.push(savedEvent.id)
    window.dataService.saveOrganizer(organizer)

    alert("Event created successfully!")
    window.location.href = "organizer-events.html"
  }

  // Function to update existing event
  function updateEvent(formData) {
    // Update event object
    const updatedEvent = {
      ...currentEvent,
      title: formData.get("eventName"),
      description: formData.get("eventDescription"),
      date: formData.get("eventDate"),
      time: formData.get("eventTime"),
      location: formData.get("eventLocation"),
      category: formData.get("eventCategory"),
      tickets: {
        general: {
          ...currentEvent.tickets.general,
          price: Number.parseFloat(formData.get("generalPrice")),
          capacity: Number.parseInt(formData.get("generalCapacity")),
        },
        vip: {
          ...currentEvent.tickets.vip,
          price: Number.parseFloat(formData.get("vipPrice")),
          capacity: Number.parseInt(formData.get("vipCapacity")),
        },
      },
    }

    // Save updated event
    window.dataService.saveEvent(updatedEvent)

    // Clear edit event ID
    sessionStorage.removeItem("editEventId")

    alert("Event updated successfully!")
    window.location.href = "organizer-events.html"
  }
})

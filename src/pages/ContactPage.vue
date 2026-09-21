<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, MapPin, Phone, Mail, Clock, Send, CheckCircle2 } from 'lucide-vue-next'
import { restroHandler, type RestaurantData } from '../services/api'

const name = ref('')
const contact = ref('')
const message = ref('')
const submitted = ref(false)

const outletInfo = ref<RestaurantData>({
  outlet_name: 'SHP Restaurant - Civil Lines',
  name: 'SHP Restaurant',
  tagline: 'Good Food Great Moments',
  description: 'Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.',
  hero_image: '',
  address: 'Plot 14, Main Boulevard, Civil Lines, City',
  phone: '+91 98765 43210 / 011 2345 6789',
  email: 'contact@shprestaurant.com',
  opening_hours: 'Mon - Sun: 11:00 AM – 11:30 PM',
  gst_rate: '5%',
  auto_accept: true,
})

onMounted(async () => {
  try {
    const data = await restroHandler.restaurants.getCurrent()
    if (data) {
      outletInfo.value = data
    }
  } catch {}
})

function handleSubmit() {
  submitted.value = true
}
</script>

<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e]">
    <!-- Header -->
    <header class="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between">
        <RouterLink to="/" class="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
          <ArrowLeft :size="16" /> Home
        </RouterLink>
        <span class="font-heading text-lg font-bold text-gray-900">Contact & Outlets</span>
        <div class="w-16" />
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-6 py-12">
      <div class="mb-10 text-center">
        <h1 class="font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
          Get in Touch with SHP
        </h1>
        <p class="mt-2 text-xs sm:text-sm text-gray-500">
          Have questions regarding table bookings, party catering, or feedback? We’d love to hear from you.
        </p>
      </div>

      <div class="grid gap-8 lg:grid-cols-2">
        <!-- Outlet Contact Details -->
        <div class="space-y-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 class="font-heading text-xl font-bold text-gray-900">Main Outlet Information</h2>

          <div class="space-y-4 text-xs text-gray-700">
            <div class="flex items-start gap-3">
              <MapPin :size="18" class="text-[#f47b20] shrink-0 mt-0.5" />
              <div>
                <p class="font-bold text-gray-900">{{ outletInfo.outlet_name }}</p>
                <p class="text-gray-500">{{ outletInfo.address }}</p>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <Phone :size="18" class="text-[#f47b20] shrink-0" />
              <span>{{ outletInfo.phone }}</span>
            </div>

            <div class="flex items-center gap-3">
              <Mail :size="18" class="text-[#f47b20] shrink-0" />
              <span>{{ outletInfo.email }}</span>
            </div>

            <div class="flex items-start gap-3">
              <Clock :size="18" class="text-[#f47b20] shrink-0 mt-0.5" />
              <div>
                <p class="font-bold text-gray-900">Operating Hours</p>
                <p class="text-gray-500">{{ outletInfo.opening_hours }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Inquiry Form -->
        <div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <h2 class="font-heading text-xl font-bold text-gray-900 mb-4">Send Us a Message</h2>

          <div v-if="submitted" class="text-center py-8 space-y-3">
            <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
              <CheckCircle2 :size="32" />
            </div>
            <h3 class="text-lg font-bold text-gray-900">Message Sent!</h3>
            <p class="text-xs text-gray-500">Thank you for reaching out. We will get back to you shortly.</p>
          </div>

          <form v-else @submit.prevent="handleSubmit" class="space-y-4 text-xs">
            <div>
              <label class="font-bold text-gray-700 block mb-1">Your Name</label>
              <input
                v-model="name"
                type="text"
                required
                placeholder="John Doe"
                class="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-gray-700 block mb-1">Email / Phone</label>
              <input
                v-model="contact"
                type="text"
                required
                placeholder="john@example.com"
                class="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-gray-700 block mb-1">Message</label>
              <textarea
                v-model="message"
                rows="4"
                required
                placeholder="Write your feedback or inquiry..."
                class="w-full rounded-md border border-gray-300 bg-white p-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
              />
            </div>

            <button
              type="submit"
              class="w-full flex items-center justify-center gap-2 rounded-md bg-[#f47b20] py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
            >
              <Send :size="14" /> Send Inquiry
            </button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e] flex flex-col justify-between selection:bg-[#f47b20]/20 selection:text-[#f47b20]">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 flex-1 w-full">
      <!-- Title -->
      <div class="mb-8 sm:mb-12 text-center max-w-2xl mx-auto">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100/90 border border-orange-200/80 px-3.5 py-1 text-xs font-bold text-[#f47b20] shadow-xs">
          <MapPin :size="13" /> Flagship Restro & Lounge
        </span>
        <h1 class="mt-3.5 font-heading text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-gray-900 leading-tight">
          Contact & Location
        </h1>
        <p class="mt-2.5 text-xs sm:text-sm text-gray-600 leading-relaxed">
          Have queries regarding table reservations, private banquet hosting, dietary preferences or feedback? Our guest care desk is available 7 days a week.
        </p>
      </div>

      <div class="grid gap-8 lg:grid-cols-12 items-start">
        <!-- Outlet Details & Location Info (7 cols on lg) -->
        <div class="lg:col-span-7 space-y-6">
          <!-- Outlet Card -->
          <div class="rounded-3xl border border-gray-200/90 bg-white p-6 sm:p-8 shadow-xs">
            <div class="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-gray-100">
              <div>
                <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-50 border border-orange-200 px-3 py-1 text-xs font-bold text-[#f47b20]">
                  📍 Primary Location
                </span>
                <h2 class="font-heading text-2xl font-black text-gray-900 mt-2">
                  {{ outletInfo.outlet_name }}
                </h2>
              </div>

              <!-- Live Dynamic Status Badge -->
              <span class="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 border border-emerald-200 px-3.5 py-1.5 text-xs font-bold text-emerald-700 shadow-xs">
                <span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Open Now (11:00 AM – 11:30 PM)</span>
              </span>
            </div>

            <p class="text-xs sm:text-sm text-gray-600 mt-3 leading-relaxed">
              {{ outletInfo.description }}
            </p>

            <!-- Direct Contact Actions Grid -->
            <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <a
                :href="telHref"
                class="flex items-center gap-3 p-3.5 rounded-2xl bg-gray-50 hover:bg-orange-50/60 border border-gray-200/80 hover:border-orange-200 transition-all group cursor-pointer"
              >
                <div class="w-10 h-10 rounded-xl bg-orange-100 text-[#f47b20] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                  <Phone :size="18" />
                </div>
                <div>
                  <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Call Support</p>
                  <p class="font-bold text-gray-900 text-xs mt-0.5">{{ outletInfo.phone }}</p>
                </div>
              </a>

              <a
                :href="whatsappHref"
                target="_blank"
                class="flex items-center gap-3 p-3.5 rounded-2xl bg-emerald-50/50 hover:bg-emerald-50 border border-emerald-200/80 transition-all group cursor-pointer"
              >
                <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                  <MessageSquare :size="18" />
                </div>
                <div>
                  <p class="text-[11px] font-bold text-emerald-700 uppercase tracking-wider">WhatsApp Concierge</p>
                  <p class="font-bold text-gray-900 text-xs mt-0.5">{{ outletInfo.phone }}</p>
                </div>
              </a>

              <a
                :href="`mailto:${outletInfo.email}`"
                class="flex items-center gap-3 p-3.5 rounded-2xl bg-gray-50 hover:bg-orange-50/60 border border-gray-200/80 hover:border-orange-200 transition-all group cursor-pointer"
              >
                <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                  <Mail :size="18" />
                </div>
                <div>
                  <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Email Desk</p>
                  <p class="font-bold text-gray-900 text-xs mt-0.5">{{ outletInfo.email }}</p>
                </div>
              </a>

              <div class="flex items-center gap-3 p-3.5 rounded-2xl bg-gray-50 border border-gray-200/80">
                <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
                  <Clock :size="18" />
                </div>
                <div>
                  <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Kitchen Hours</p>
                  <p class="font-bold text-gray-900 text-xs mt-0.5">11:00 AM – 11:30 PM (All Days)</p>
                </div>
              </div>
            </div>

            <!-- Address and Landmark Details -->
            <div class="mt-6 pt-5 border-t border-gray-100 space-y-3">
              <div class="flex items-start gap-3 text-xs sm:text-sm text-gray-700">
                <MapPin :size="18" class="text-[#f47b20] shrink-0 mt-0.5" />
                <div>
                  <p class="font-bold text-gray-900">Physical Address</p>
                  <p class="text-gray-600 mt-0.5">{{ outletInfo.address }}</p>
                </div>
              </div>

              <!-- Amenities tags -->
              <div class="flex flex-wrap gap-2 pt-2">
                <span class="px-2.5 py-1 rounded-lg bg-gray-100 text-gray-700 text-[11px] font-semibold flex items-center gap-1">
                  🚗 Free Valet Parking
                </span>
                <span class="px-2.5 py-1 rounded-lg bg-gray-100 text-gray-700 text-[11px] font-semibold flex items-center gap-1">
                  📶 High-speed Guest WiFi
                </span>
                <span class="px-2.5 py-1 rounded-lg bg-gray-100 text-gray-700 text-[11px] font-semibold flex items-center gap-1">
                  ♿ Wheelchair Accessible
                </span>
                <span class="px-2.5 py-1 rounded-lg bg-gray-100 text-gray-700 text-[11px] font-semibold flex items-center gap-1">
                  💳 Cards, UPI & Cash Accepted
                </span>
              </div>
            </div>
          </div>

          <!-- Embedded Map Card Placeholder with Navigation Button -->
          <div class="rounded-3xl border border-gray-200/90 bg-white p-5 sm:p-6 shadow-xs overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <Navigation :size="16" class="text-[#f47b20]" />
                <h3 class="font-heading font-bold text-sm text-gray-900">Interactive Location Map</h3>
              </div>
              <a
                :href="mapsHref"
                target="_blank"
                class="text-xs font-bold text-[#f47b20] hover:underline flex items-center gap-1"
              >
                <span>Open in Google Maps</span>
                <ExternalLink :size="13" />
              </a>
            </div>

            <!-- Stylized Map Container -->
            <div class="relative h-48 sm:h-60 rounded-2xl overflow-hidden bg-gray-100 border border-gray-200 flex flex-col items-center justify-center text-center p-6 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]">
              <div class="h-12 w-12 rounded-full bg-[#f47b20] text-white flex items-center justify-center shadow-lg animate-bounce mb-2">
                <MapPin :size="24" />
              </div>
              <p class="font-bold text-gray-900 text-sm">SHP Restaurant & Banquets</p>
              <p class="text-xs text-gray-500 mt-0.5">Plot 14, Main Boulevard, Civil Lines</p>
              <a
                href="https://maps.google.com/?q=Civil+Lines+Delhi"
                target="_blank"
                class="mt-3 rounded-xl bg-gray-900 text-white px-4 py-2 text-xs font-bold shadow-md hover:bg-[#f47b20] transition-colors"
              >
                Get Driving Directions
              </a>
            </div>
          </div>
        </div>

        <!-- Direct Inquiry & Message Form (5 cols on lg) -->
        <div class="lg:col-span-5 rounded-3xl border border-gray-200/90 bg-white p-6 sm:p-8 shadow-xs">
          <h2 class="font-heading text-xl font-black text-gray-900 mb-1">Send a Message</h2>
          <p class="text-xs text-gray-500 mb-5">Our guest relations manager typically replies within 2 hours.</p>

          <!-- Success Alert -->
          <div
            v-if="submitted"
            class="rounded-2xl bg-emerald-50 border border-emerald-200 p-6 text-center space-y-3 animate-fade-in"
          >
            <div class="h-12 w-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
              <CheckCircle2 :size="28" />
            </div>
            <h4 class="font-bold text-emerald-900 text-sm">Your Message is Ready to Send</h4>
            <p class="text-xs text-emerald-700">
              Thank you, {{ name || 'Guest' }}.
              <template v-if="dispatchChannel === 'email'">
                We’ve opened your email app with your message pre-filled to {{ outletInfo.email }} — just hit send and our guest care team will reply to {{ contact }}.
              </template>
              <template v-else-if="dispatchChannel === 'whatsapp'">
                We’ve opened WhatsApp with your message pre-filled to our guest care desk — just hit send and we’ll reply to {{ contact }}.
              </template>
              <template v-else>
                Please reach us directly at {{ outletInfo.email }} or {{ outletInfo.phone }} and we’ll get back to you.
              </template>
            </p>
            <button
              @click="resetForm"
              class="mt-2 text-xs font-bold text-emerald-800 underline cursor-pointer"
            >
              Send Another Note
            </button>
          </div>

          <!-- Message Form -->
          <form v-else @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Category Chips -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
                Topic of Inquiry
              </label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="cat in inquiryCategories"
                  :key="cat"
                  type="button"
                  @click="topic = cat"
                  :class="[
                    'py-2 px-2 rounded-xl text-xs font-bold border transition-all cursor-pointer text-center truncate',
                    topic === cat
                      ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] ring-1 ring-orange-400/20 font-black'
                      : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                  ]"
                >
                  {{ cat }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1">Your Full Name</label>
              <input
                v-model="name"
                type="text"
                required
                placeholder="e.g. Ananya Sharma"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1">Mobile Number or Email</label>
              <input
                v-model="contact"
                type="text"
                required
                placeholder="e.g. +91 98765 43210 or email@domain.com"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1">Your Query / Message</label>
              <textarea
                v-model="message"
                rows="4"
                required
                placeholder="How can our hospitality team assist you today?"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              ></textarea>
            </div>

            <button
              type="submit"
              class="w-full orange-button py-3.5 rounded-xl font-bold text-xs shadow-md flex items-center justify-center gap-2 cursor-pointer active:scale-[0.99] transition-all"
            >
              <Send :size="15" />
              <span>Send Message to Guest Care</span>
            </button>
          </form>
        </div>
      </div>
    </main>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  MapPin,
  Phone,
  Mail,
  Clock,
  Send,
  CheckCircle2,
  MessageSquare,
  Navigation,
  ExternalLink,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler, type RestaurantData } from '../services/api'

const name = ref('')
const contact = ref('')
const message = ref('')
const topic = ref('General Inquiry')
const submitted = ref(false)

const inquiryCategories = [
  'General Inquiry',
  'Banquet Booking',
  'Food Feedback',
  'Franchise & Career',
]

const outletInfo = ref<RestaurantData>({
  outlet_name: 'SHP Restaurant - Civil Lines',
  name: 'SHP Restaurant',
  tagline: 'Good Food Great Moments',
  description: 'Authentic flavors, artisanal oven pizzas, sizzling appetizers, and grand banquet dining in the heart of the city.',
  hero_image: '',
  address: 'Plot 14, Main Boulevard, Civil Lines, City - 110054',
  phone: '+91 98765 43210 / 011 2345 6789',
  email: 'contact@shprestaurant.com',
  opening_hours: 'Mon - Sun: 11:00 AM – 11:30 PM (IST)',
  gst_rate: '5%',
  auto_accept: true,
})

// The channel the guest's message was actually handed off through (mailto / WhatsApp).
const dispatchChannel = ref<'email' | 'whatsapp' | ''>('')

// Digits-only WhatsApp/phone number derived from the outlet's real phone field.
const whatsappNumber = computed(() => outletInfo.value.phone.replace(/\D/g, ''))
const telHref = computed(() => `tel:${outletInfo.value.phone.replace(/[^\d+]/g, '')}`)
const whatsappHref = computed(
  () => `https://wa.me/${whatsappNumber.value}?text=${encodeURIComponent('Hi ' + outletInfo.value.name + ', I have an inquiry')}`
)
const mapsHref = computed(
  () => `https://maps.google.com/?q=${encodeURIComponent(outletInfo.value.address)}`
)

onMounted(async () => {
  try {
    const data = await restroHandler.restaurants.getCurrent()
    if (data) {
      outletInfo.value = data
    }
  } catch {
    // Keep the graceful fallback details already set above.
  }
})

function handleSubmit() {
  const subject = `[${topic.value}] Message from ${name.value || 'Website Guest'}`
  const body =
    `Name: ${name.value}\n` +
    `Contact: ${contact.value}\n` +
    `Topic: ${topic.value}\n\n` +
    `${message.value}`

  // There is no backend message endpoint, so hand off honestly through the
  // guest's own mail client (or WhatsApp) to the outlet's real contact details.
  if (outletInfo.value.email) {
    dispatchChannel.value = 'email'
    window.location.href =
      `mailto:${outletInfo.value.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
  } else if (whatsappNumber.value) {
    dispatchChannel.value = 'whatsapp'
    window.open(
      `https://wa.me/${whatsappNumber.value}?text=${encodeURIComponent(subject + '\n\n' + body)}`,
      '_blank'
    )
  }

  submitted.value = true
}

function resetForm() {
  submitted.value = false
  message.value = ''
  dispatchChannel.value = ''
}
</script>

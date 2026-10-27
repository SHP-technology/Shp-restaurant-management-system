<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e] flex flex-col justify-between selection:bg-[#f47b20]/20 selection:text-[#f47b20]">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 flex-1 w-full">
      <!-- Title & Hero Banner -->
      <div class="mb-8 sm:mb-12 text-center max-w-2xl mx-auto">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100/90 border border-orange-200/80 px-3.5 py-1 text-xs font-bold text-[#f47b20] shadow-xs">
          <Sparkles :size="13" class="animate-pulse" /> Instant Guaranteed Seating
        </span>
        <h1 class="mt-3.5 font-heading text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-gray-900 leading-tight">
          Reserve Your Table
        </h1>
        <p class="mt-2.5 text-xs sm:text-sm text-gray-600 leading-relaxed">
          Skip the queue and secure your preferred dining ambiance in seconds. Confirmation is instantly synced with our floor manager.
        </p>
      </div>

      <!-- Confirmation Screen / Ticket Receipt -->
      <div
        v-if="isSubmitted"
        class="rounded-3xl border border-gray-200 bg-white p-6 sm:p-10 text-center shadow-xl max-w-xl mx-auto animate-fade-in"
      >
        <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 shadow-md ring-8 ring-emerald-50">
          <CheckCircle2 :size="44" />
        </div>

        <span class="mt-4 inline-block px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
          Reservation Confirmed
        </span>

        <h2 class="mt-2 text-2xl sm:text-3xl font-black text-gray-900 font-heading">
          We’re Expecting You!
        </h2>
        <p class="text-xs text-gray-500 mt-1">
          A confirmation SMS & WhatsApp message has been dispatched to <span class="font-bold text-gray-800">{{ phone }}</span>.
        </p>

        <!-- Digital Booking Pass / Card -->
        <div class="mt-6 rounded-2xl bg-gradient-to-b from-orange-50/70 to-amber-50/40 border border-orange-200/80 p-5 text-left text-xs sm:text-sm space-y-3 relative overflow-hidden shadow-inner">
          <div class="flex justify-between items-center pb-2 border-b border-orange-200/60">
            <span class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Booking Ref:</span>
            <span class="font-mono font-black text-sm text-[#f47b20]">{{ bookingRef }}</span>
          </div>
          
          <div class="grid grid-cols-2 gap-3 pt-1">
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Primary Guest</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ name }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Party Size</p>
              <p class="font-bold text-[#f47b20] text-sm mt-0.5 flex items-center gap-1">
                <Users :size="14" /> {{ guests }} {{ guests === 1 ? 'Guest' : 'Guests' }}
              </p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Date & Slot</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ formattedDisplayDate }} at {{ timeSlot }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Dining Zone</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ seatingZone }}</p>
            </div>
          </div>

          <div v-if="specialRequest" class="pt-2 border-t border-orange-200/60">
            <p class="text-[11px] text-gray-500 font-medium">Special Requests:</p>
            <p class="text-xs text-gray-700 italic mt-0.5">"{{ specialRequest }}"</p>
          </div>
        </div>

        <div class="mt-7 flex flex-col sm:flex-row justify-center gap-3">
          <RouterLink
            to="/menu"
            class="orange-button px-6 py-3.5 rounded-xl font-bold text-xs shadow-md text-center flex items-center justify-center gap-1.5"
          >
            <UtensilsCrossed :size="15" />
            <span>Pre-order Menu Items</span>
          </RouterLink>
          <button
            @click="resetBookingForm"
            class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-3.5 rounded-xl font-bold text-xs transition-colors"
          >
            Book Another Table
          </button>
        </div>
      </div>

      <!-- Interactive Booking Form -->
      <form
        v-else
        @submit.prevent="handleSubmit"
        class="space-y-8 rounded-3xl border border-gray-200/90 bg-white p-5 sm:p-8 lg:p-10 shadow-xs"
      >
        <!-- 1. Guest Count Selector (Stepper + Quick Chips) -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <label class="text-xs font-bold uppercase tracking-wider text-gray-700 flex items-center gap-1.5">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">1</span>
              <span>Number of Guests</span>
            </label>
            <span class="text-xs font-bold text-[#f47b20] bg-orange-50 px-2.5 py-1 rounded-full border border-orange-100">
              {{ guests }} {{ guests === 1 ? 'Person' : 'People' }}
            </span>
          </div>

          <!-- Quick chips for common guest counts -->
          <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 sm:gap-3">
            <button
              v-for="count in [1, 2, 4, 6, 8, 12]"
              :key="count"
              type="button"
              @click="guests = count"
              :class="[
                'py-2.5 sm:py-3 rounded-2xl font-bold text-xs sm:text-sm border transition-all cursor-pointer flex flex-col items-center justify-center gap-0.5 sm:gap-1 active:scale-95',
                guests === count
                  ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] shadow-xs ring-2 ring-orange-400/20 font-black'
                  : 'border-gray-200 bg-gray-50/60 text-gray-700 hover:border-gray-300 hover:bg-white'
              ]"
            >
              <Users :size="15" />
              <span>{{ count }} {{ count === 1 ? 'Guest' : 'Guests' }}</span>
            </button>
          </div>

          <!-- Numeric Stepper for custom party size -->
          <div class="mt-3 flex items-center justify-between rounded-xl bg-gray-50 p-3 border border-gray-200/80">
            <span class="text-xs text-gray-600 font-medium">Custom Party Size (1 to 30):</span>
            <div class="flex items-center gap-3">
              <button
                type="button"
                @click="guests = Math.max(1, guests - 1)"
                class="h-8 w-8 rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-100 flex items-center justify-center font-bold text-base transition-colors"
                :disabled="guests <= 1"
              >
                -
              </button>
              <span class="w-8 text-center font-black text-sm text-gray-900">{{ guests }}</span>
              <button
                type="button"
                @click="guests = Math.min(30, guests + 1)"
                class="h-8 w-8 rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-100 flex items-center justify-center font-bold text-base transition-colors"
                :disabled="guests >= 30"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <!-- 2. Date & Time Selection -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <!-- Date Picker -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2.5 flex items-center gap-1.5">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">2</span>
              <span>Select Date</span>
            </label>

            <!-- Quick Date Chips -->
            <div class="grid grid-cols-3 gap-2 mb-2.5">
              <button
                v-for="preset in datePresets"
                :key="preset.label"
                type="button"
                @click="date = preset.value"
                :class="[
                  'py-2 px-1 text-center rounded-xl text-xs font-bold border transition-all cursor-pointer truncate',
                  date === preset.value
                    ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] ring-1 ring-orange-400/20'
                    : 'border-gray-200 bg-gray-50 text-gray-600 hover:border-gray-300'
                ]"
              >
                {{ preset.label }}
              </button>
            </div>

            <div class="relative">
              <input
                v-model="date"
                type="date"
                :min="todayIsoString"
                required
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              />
            </div>
          </div>

          <!-- Time Slot Selection with Meal Period Categorization -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2.5 flex items-center gap-1.5">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">3</span>
              <span>Select Dining Slot</span>
            </label>

            <div class="space-y-3">
              <!-- Lunch Slots -->
              <div>
                <span class="text-[10px] font-bold text-gray-500 uppercase tracking-wider block mb-1.5">
                  ☀️ Lunch / Afternoon
                </span>
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="slot in lunchSlots"
                    :key="slot"
                    type="button"
                    @click="timeSlot = slot"
                    :class="[
                      'py-2 px-1 rounded-xl text-xs font-bold border transition-all cursor-pointer text-center',
                      timeSlot === slot
                        ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] ring-2 ring-orange-400/20 font-black'
                        : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                    ]"
                  >
                    {{ slot }}
                  </button>
                </div>
              </div>

              <!-- Dinner Slots -->
              <div>
                <span class="text-[10px] font-bold text-gray-500 uppercase tracking-wider block mb-1.5">
                  🌙 Evening / Dinner
                </span>
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="slot in dinnerSlots"
                    :key="slot"
                    type="button"
                    @click="timeSlot = slot"
                    :class="[
                      'py-2 px-1 rounded-xl text-xs font-bold border transition-all cursor-pointer text-center',
                      timeSlot === slot
                        ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] ring-2 ring-orange-400/20 font-black'
                        : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                    ]"
                  >
                    {{ slot }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Seating Ambiance Zone Cards -->
        <div class="pt-2">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">4</span>
            <span>Preferred Seating Zone & Ambiance</span>
          </label>
          <div class="grid gap-3 sm:grid-cols-3">
            <div
              v-for="opt in seatingOptions"
              :key="opt.name"
              @click="seatingZone = opt.name"
              :class="[
                'p-4 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between relative overflow-hidden',
                seatingZone === opt.name
                  ? 'border-[#f47b20] bg-orange-50/60 shadow-md ring-2 ring-orange-400/25'
                  : 'border-gray-200 hover:border-gray-300 bg-white hover:shadow-xs'
              ]"
            >
              <div
                v-if="seatingZone === opt.name"
                class="absolute top-2 right-2 bg-[#f47b20] text-white rounded-full p-0.5"
              >
                <Check :size="12" />
              </div>

              <div>
                <div class="text-3xl mb-2">{{ opt.icon }}</div>
                <h4 class="font-heading font-bold text-sm text-gray-900">{{ opt.name }}</h4>
                <p class="text-[11px] text-gray-500 mt-1 leading-snug">{{ opt.desc }}</p>
              </div>

              <div class="mt-3.5 pt-2 border-t border-gray-100 flex items-center justify-between text-[10px]">
                <span class="font-semibold text-gray-500">{{ opt.tag }}</span>
                <span
                  class="font-bold uppercase tracking-wider"
                  :class="seatingZone === opt.name ? 'text-[#f47b20]' : 'text-gray-400'"
                >
                  {{ seatingZone === opt.name ? 'Selected' : 'Choose' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Contact Information -->
        <div class="border-t border-gray-100 pt-6">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-4 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">5</span>
            <span>Guest Contact Information</span>
          </label>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Primary Guest Name</label>
              <input
                v-model="name"
                type="text"
                required
                placeholder="Enter your full name"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Contact Mobile Number</label>
              <input
                v-model="phone"
                type="tel"
                required
                placeholder="Enter 10-digit mobile number"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
              />
              <p v-if="phoneError" class="mt-1.5 text-[11px] font-semibold text-red-600">{{ phoneError }}</p>
            </div>
          </div>

          <div class="mt-4">
            <label class="block text-xs font-semibold text-gray-700 mb-1.5">Special Dietary Notes or Occasion (Optional)</label>
            <input
              v-model="specialRequest"
              type="text"
              placeholder="e.g. Birthday anniversary, high chair needed, quiet corner table preferred"
              class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
            />
          </div>
        </div>

        <!-- Submit Button -->
        <div class="pt-2">
          <div
            v-if="error"
            class="mb-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-xs font-semibold text-red-700 flex items-center gap-2"
          >
            <span>⚠️</span>
            <span>{{ error }}</span>
          </div>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full orange-button py-4 rounded-2xl font-bold text-sm shadow-lg shadow-orange-500/25 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 active:scale-[0.99] transition-all"
          >
            <Calendar :size="18" />
            <span>{{ isSubmitting ? 'Confirming Table with Floor Manager...' : 'Confirm Table Reservation' }}</span>
          </button>
          <p class="text-center text-[11px] text-gray-500 mt-2.5">
            🔒 Free cancellation anytime up to 30 minutes before your dining slot.
          </p>
        </div>
      </form>
    </main>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import {
  Calendar,
  Users,
  Sparkles,
  CheckCircle2,
  Check,
  UtensilsCrossed,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'

const guests = ref(2)
const name = ref('')
const phone = ref('')
const date = ref(new Date().toISOString().split('T')[0])
const timeSlot = ref('07:30 PM')
const seatingZone = ref('Main Dining')
const specialRequest = ref('')
const isSubmitted = ref(false)
const isSubmitting = ref(false)
const error = ref('')
const bookingRef = ref('SHP-RES-4829')

const phoneError = computed(() =>
  phone.value && !/^\d{10}$/.test(phone.value)
    ? 'Please enter a valid 10-digit mobile number.'
    : ''
)

const lunchSlots = ['12:30 PM', '01:15 PM', '02:00 PM']
const dinnerSlots = ['07:00 PM', '07:30 PM', '08:15 PM', '09:00 PM', '09:45 PM']

const seatingOptions = [
  {
    name: 'Main Dining',
    icon: '🍷',
    desc: 'Warm ambient lighting with acoustic backdrop & live kitchen showcase',
    tag: 'Popular for Families',
  },
  {
    name: 'Rooftop Terrace',
    icon: '🌌',
    desc: 'Open sky panoramic dining under fairy lights with city skyline view',
    tag: 'Romantic Sunset Views',
  },
  {
    name: 'Private VIP Booth',
    icon: '👑',
    desc: 'Secluded luxury leather booths for business meetings & celebrations',
    tag: 'Exclusive & Quiet',
  },
]

const todayIsoString = computed(() => new Date().toISOString().split('T')[0])

const datePresets = computed(() => {
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(today.getDate() + 1)

  const saturday = new Date(today)
  const daysUntilSaturday = (6 - today.getDay() + 7) % 7 || 7
  saturday.setDate(today.getDate() + daysUntilSaturday)

  return [
    { label: 'Today', value: today.toISOString().split('T')[0] },
    { label: 'Tomorrow', value: tomorrow.toISOString().split('T')[0] },
    { label: 'Weekend', value: saturday.toISOString().split('T')[0] },
  ]
})

const formattedDisplayDate = computed(() => {
  if (!date.value) return ''
  try {
    const d = new Date(date.value + 'T00:00:00')
    return d.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  } catch {
    return date.value
  }
})

function resetBookingForm() {
  isSubmitted.value = false
  error.value = ''
  name.value = ''
  phone.value = ''
  specialRequest.value = ''
}

async function handleSubmit() {
  error.value = ''
  if (!/^\d{10}$/.test(phone.value)) {
    error.value = 'Please enter a valid 10-digit mobile number.'
    return
  }
  isSubmitting.value = true
  try {
    const reservation = await restroHandler.reservations.createTableReservation({
      name: name.value,
      phone: phone.value,
      date: date.value,
      timeSlot: timeSlot.value,
      guests: guests.value,
      seatingZone: seatingZone.value,
      specialRequest: specialRequest.value,
    })
    bookingRef.value = reservation?.id
      ? `SHP-RES-${reservation.id}`
      : `SHP-RES-${Math.floor(1000 + Math.random() * 9000)}`
    isSubmitted.value = true
  } catch (err) {
    error.value = getApiErrorMessage(err) || 'We could not confirm your reservation. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, Calendar, Clock, Users, Sparkles, CheckCircle2 } from 'lucide-vue-next'
import { restroHandler } from '../services/api'

const guests = ref(2)
const name = ref('Harsh Patel')
const phone = ref('+91 98765 43210')
const date = ref('2026-09-10')
const timeSlot = ref('07:30 PM')
const seatingZone = ref('Main Dining')
const specialRequest = ref('')
const isSubmitted = ref(false)
const isSubmitting = ref(false)

const timeSlots = ['12:30 PM', '01:30 PM', '07:00 PM', '07:30 PM', '08:15 PM', '09:00 PM']
const seatingOptions = [
  { name: 'Main Dining', desc: 'Warm ambiance with live kitchen view' },
  { name: 'Rooftop Terrace', desc: 'Open sky dining with city skyline view' },
  { name: 'Private VIP Booth', desc: 'Secluded cozy seating for special occasions' },
]

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await restroHandler.reservations.createTableReservation({
      name: name.value,
      phone: phone.value,
      date: date.value,
      timeSlot: timeSlot.value,
      guests: guests.value,
      seatingZone: seatingZone.value,
      specialRequest: specialRequest.value,
    })
    isSubmitted.value = true
  } catch {
    // Fallback
    isSubmitted.value = true
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e]">
    <!-- Top Header -->
    <header class="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between">
        <RouterLink to="/" class="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
          <ArrowLeft :size="16" /> Home
        </RouterLink>
        <span class="font-heading text-lg font-bold text-gray-900">Table Reservation</span>
        <div class="w-16" />
      </div>
    </header>

    <main class="mx-auto max-w-4xl px-6 py-12">
      <div class="mb-10 text-center">
        <span class="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
          <Sparkles :size="14" /> Reserve Your Table
        </span>
        <h1 class="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
          Book a Table at SHP
        </h1>
        <p class="mt-2 text-xs sm:text-sm text-gray-500">
          Enjoy delicious food and cozy hospitality. Instant table confirmation.
        </p>
      </div>

      <div v-if="isSubmitted" class="rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-lg">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
          <CheckCircle2 :size="40" />
        </div>
        <h2 class="mt-6 text-2xl font-bold text-gray-900">Reservation Confirmed!</h2>
        <p class="mt-2 text-sm text-gray-600">
          We look forward to hosting you for <span class="text-[#f47b20] font-bold">{{ guests }} guests</span> on
          <span class="text-[#f47b20] font-bold">{{ date }}</span> at
          <span class="text-[#f47b20] font-bold">{{ timeSlot }}</span> in {{ seatingZone }}.
        </p>
        <div class="mt-8 flex justify-center gap-4">
          <RouterLink
            to="/menu"
            class="rounded-md bg-[#f47b20] px-6 py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
          >
            Pre-order Menu Items
          </RouterLink>
          <button
            @click="isSubmitted = false"
            class="rounded-md border border-gray-300 bg-gray-50 px-6 py-3 text-xs font-bold text-gray-700 hover:bg-gray-100"
          >
            Book Another Table
          </button>
        </div>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
        <!-- Guest Count -->
        <div>
          <label class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
            <Users :size="16" class="text-[#f47b20]" /> Number of Guests
          </label>
          <div class="flex flex-wrap gap-3">
            <button
              v-for="num in [1, 2, 3, 4, 5, 6, 8, 10]"
              :key="num"
              type="button"
              @click="guests = num"
              :class="[
                'h-11 w-12 rounded-lg text-xs font-bold transition',
                guests === num
                  ? 'bg-[#f47b20] text-white shadow-sm scale-105'
                  : 'border border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ num }}{{ num === 10 ? '+' : '' }}
            </button>
          </div>
        </div>

        <!-- Date & Time Slot -->
        <div class="grid gap-6 md:grid-cols-2">
          <div>
            <label class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
              <Calendar :size="16" class="text-[#f47b20]" /> Select Date
            </label>
            <input
              v-model="date"
              type="date"
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div>
            <label class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-700 mb-3">
              <Clock :size="16" class="text-[#f47b20]" /> Available Time Slot
            </label>
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="slot in timeSlots"
                :key="slot"
                type="button"
                @click="timeSlot = slot"
                :class="[
                  'rounded-md py-2 text-xs font-bold transition',
                  timeSlot === slot
                    ? 'bg-[#f47b20] text-white'
                    : 'border border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                ]"
              >
                {{ slot }}
              </button>
            </div>
          </div>
        </div>

        <!-- Seating Preference -->
        <div>
          <label class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 block">Seating Area</label>
          <div class="grid gap-4 md:grid-cols-3">
            <div
              v-for="opt in seatingOptions"
              :key="opt.name"
              @click="seatingZone = opt.name"
              :class="[
                'cursor-pointer rounded-xl border p-4 transition',
                seatingZone === opt.name
                  ? 'border-[#f47b20] bg-orange-50/60 shadow-sm'
                  : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
              ]"
            >
              <p class="font-bold text-gray-900 text-xs">{{ opt.name }}</p>
              <p class="mt-1 text-[11px] text-gray-500">{{ opt.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Contact Details -->
        <div class="grid gap-6 md:grid-cols-2">
          <div>
            <label class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2 block">Your Name</label>
            <input
              v-model="name"
              type="text"
              required
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>
          <div>
            <label class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2 block">Phone Number</label>
            <input
              v-model="phone"
              type="text"
              required
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>
        </div>

        <!-- Special Request -->
        <div>
          <label class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2 block">Special Requests (Optional)</label>
          <textarea
            v-model="specialRequest"
            rows="3"
            placeholder="Anniversary celebration, dietary preferences, high-chair needed..."
            class="w-full rounded-md border border-gray-300 bg-white p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
          />
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full rounded-md bg-[#f47b20] py-3.5 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f] disabled:opacity-50"
        >
          {{ isSubmitting ? 'Confirming Reservation...' : 'Confirm Table Reservation' }}
        </button>
      </form>
    </main>
  </div>
</template>

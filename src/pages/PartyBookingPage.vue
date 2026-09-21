<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, Users, Gift, Cake, Sparkles, CheckCircle2 } from 'lucide-vue-next'
import { restroHandler } from '../services/api'

const occasion = ref('Birthday Celebration')
const guestCount = ref('25-50 Guests')
const date = ref('2026-10-15')
const clientName = ref('Pooja Kapoor')
const phone = ref('+91 98765 43210')
const requirements = ref('Decoration, Cake, Music')
const submitted = ref(false)
const isSubmitting = ref(false)

const occasions = [
  { title: 'Birthday Bash', icon: Cake, desc: 'Custom cake, balloon decor & music setup' },
  { title: 'Corporate Gala', icon: Users, desc: 'Private dining, podium & cocktail service' },
  { title: 'Anniversary & Party', icon: Gift, desc: 'Candlelight setup & live music' },
  { title: 'Custom Event', icon: Sparkles, desc: 'Bespoke menu & complete venue booking' },
]

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await restroHandler.reservations.createPartyBooking({
      occasion: occasion.value,
      client: clientName.value,
      phone: phone.value,
      date: date.value,
      guestCount: guestCount.value,
      requirements: requirements.value,
    })
    submitted.value = true
  } catch {
    submitted.value = true
  } finally {
    isSubmitting.value = false
  }
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
        <span class="font-heading text-lg font-bold text-gray-900">Party Booking</span>
        <div class="w-16" />
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-6 py-12">
      <div class="mb-10 text-center">
        <span class="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
          <Sparkles :size="14" /> Memorable Gatherings
        </span>
        <h1 class="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
          Host Your Event with Us
        </h1>
        <p class="mt-2 text-xs sm:text-sm text-gray-500">
          From birthday bashes to corporate dinners. Tailored catering and event management.
        </p>
      </div>

      <div v-if="submitted" class="rounded-2xl border border-gray-200 bg-white p-10 text-center shadow-lg max-w-xl mx-auto">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
          <CheckCircle2 :size="40" />
        </div>
        <h2 class="mt-6 text-2xl font-bold text-gray-900">Inquiry Submitted!</h2>
        <p class="mt-3 text-sm text-gray-600">
          Thank you for booking your <span class="text-[#f47b20] font-bold">{{ occasion }}</span> on
          <span class="text-[#f47b20] font-bold">{{ date }}</span>.
        </p>
        <p class="mt-2 text-xs text-gray-500">
          Our event manager will contact you within 2 hours to confirm menu and decor details.
        </p>
        <div class="mt-8">
          <RouterLink
            to="/"
            class="rounded-md bg-[#f47b20] px-6 py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
          >
            Return to Home
          </RouterLink>
        </div>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
        <!-- Occasion cards -->
        <div>
          <label class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-4 block">Select Occasion Type</label>
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div
              v-for="occ in occasions"
              :key="occ.title"
              @click="occasion = occ.title"
              :class="[
                'cursor-pointer rounded-xl border p-5 transition',
                occasion === occ.title
                  ? 'border-[#f47b20] bg-orange-50/70 shadow-sm'
                  : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
              ]"
            >
              <component
                :is="occ.icon"
                :size="24"
                :class="['mb-3', occasion === occ.title ? 'text-[#f47b20]' : 'text-gray-400']"
              />
              <p class="font-bold text-gray-900 text-xs">{{ occ.title }}</p>
              <p class="mt-1 text-[11px] text-gray-500 leading-relaxed">{{ occ.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Inputs -->
        <div class="grid gap-6 md:grid-cols-2">
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Expected Guests
            </label>
            <select
              v-model="guestCount"
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            >
              <option>10 - 25 Guests</option>
              <option>25 - 50 Guests</option>
              <option>50 - 100 Guests</option>
              <option>100+ Exclusive Hall Booking</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Event Date
            </label>
            <input
              v-model="date"
              type="date"
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Client / Organizer Name
            </label>
            <input
              v-model="clientName"
              type="text"
              required
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Contact Phone Number
            </label>
            <input
              v-model="phone"
              type="text"
              required
              class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
            Special Requirements & Setup
          </label>
          <input
            v-model="requirements"
            type="text"
            placeholder="Decoration, Cake, Music, Microphone setup..."
            class="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
          />
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full rounded-md bg-[#f47b20] py-3.5 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f] disabled:opacity-50"
        >
          {{ isSubmitting ? 'Submitting Inquiry...' : 'Submit Party Booking Request' }}
        </button>
      </form>
    </main>
  </div>
</template>

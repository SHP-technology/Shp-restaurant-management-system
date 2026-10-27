<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e] flex flex-col justify-between selection:bg-[#f47b20]/20 selection:text-[#f47b20]">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 flex-1 w-full">
      <!-- Title Header -->
      <div class="mb-8 sm:mb-12 text-center max-w-2xl mx-auto">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100/90 border border-orange-200/80 px-3.5 py-1 text-xs font-bold text-[#f47b20] shadow-xs">
          <Sparkles :size="13" class="animate-pulse" /> Grand Celebrations & Banquets
        </span>
        <h1 class="mt-3.5 font-heading text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-gray-900 leading-tight">
          Host Your Special Event
        </h1>
        <p class="mt-2.5 text-xs sm:text-sm text-gray-600 leading-relaxed">
          From birthday bashes to corporate banquets, our event planners craft bespoke gourmet menus, sound & stage setups, and unforgettable hospitality.
        </p>
      </div>

      <!-- Submitted Inquiry Receipt Card -->
      <div
        v-if="submitted"
        class="rounded-3xl border border-gray-200 bg-white p-6 sm:p-10 text-center shadow-xl max-w-xl mx-auto animate-fade-in"
      >
        <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 shadow-md ring-8 ring-emerald-50">
          <CheckCircle2 :size="44" />
        </div>

        <span class="mt-4 inline-block px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">
          Inquiry Successfully Dispatched
        </span>

        <h2 class="mt-2 text-2xl sm:text-3xl font-black text-gray-900 font-heading">
          Party Request Received!
        </h2>
        
        <div class="mt-6 rounded-2xl bg-gradient-to-b from-orange-50/70 to-amber-50/40 border border-orange-200/80 p-5 text-left text-xs sm:text-sm space-y-3 relative overflow-hidden shadow-inner">
          <div class="flex justify-between items-center pb-2 border-b border-orange-200/60">
            <span class="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Inquiry ID:</span>
            <span class="font-mono font-black text-sm text-[#f47b20]">{{ partyRef }}</span>
          </div>

          <div class="grid grid-cols-2 gap-3 pt-1">
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Occasion Type</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ occasion }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Guest Range</p>
              <p class="font-bold text-[#f47b20] text-sm mt-0.5">{{ guestCount }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Host / Organizer</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ clientName }}</p>
            </div>
            <div>
              <p class="text-[11px] text-gray-500 font-medium">Planned Date</p>
              <p class="font-bold text-gray-900 text-sm mt-0.5">{{ date }}</p>
            </div>
          </div>

          <div class="pt-2 border-t border-orange-200/60">
            <p class="text-[11px] text-gray-500 font-medium">Package Tier & Add-ons:</p>
            <p class="text-xs font-semibold text-gray-800 mt-0.5">{{ selectedPackage }} Package • {{ requirements || 'Standard Inclusions' }}</p>
          </div>
        </div>

        <div class="mt-4 rounded-xl bg-gray-50 border border-gray-200 p-3.5 text-xs text-gray-600 text-left flex items-start gap-2.5">
          <PhoneCall :size="16" class="text-[#f47b20] shrink-0 mt-0.5" />
          <p>
            Our Event Director will call you at <span class="font-bold text-gray-900">{{ phone }}</span> within 2 hours with customized menu pricing & floor layout previews.
          </p>
        </div>

        <div class="mt-7 flex flex-col sm:flex-row justify-center gap-3">
          <a
            :href="`https://wa.me/919876543210?text=Hello,%20I%20just%20submitted%20party%20booking%20inquiry%20${partyRef}%20for%20${encodeURIComponent(occasion)}`"
            target="_blank"
            class="orange-button px-6 py-3.5 rounded-xl font-bold text-xs shadow-md inline-flex items-center justify-center gap-1.5"
          >
            <MessageSquare :size="15" />
            <span>Chat with Event Planner</span>
          </a>
          <button
            @click="resetPartyForm"
            class="bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-3.5 rounded-xl font-bold text-xs transition-colors"
          >
            Submit Another Request
          </button>
        </div>
      </div>

      <!-- Event Inquiry Form -->
      <form
        v-else
        @submit.prevent="handleSubmit"
        class="space-y-8 rounded-3xl border border-gray-200/90 bg-white p-5 sm:p-8 lg:p-10 shadow-xs"
      >
        <!-- 1. Occasion Type Selection -->
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">1</span>
            <span>Select Event Occasion Type</span>
          </label>
          <div class="grid gap-3.5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
            <div
              v-for="occ in occasions"
              :key="occ.title"
              @click="occasion = occ.title"
              :class="[
                'p-4 sm:p-5 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between relative overflow-hidden',
                occasion === occ.title
                  ? 'border-[#f47b20] bg-orange-50/60 shadow-md ring-2 ring-orange-400/25'
                  : 'border-gray-200 hover:border-gray-300 bg-white hover:shadow-xs'
              ]"
            >
              <div
                v-if="occasion === occ.title"
                class="absolute top-2.5 right-2.5 bg-[#f47b20] text-white rounded-full p-0.5"
              >
                <Check :size="12" />
              </div>

              <div>
                <div class="text-3xl mb-2">{{ occ.emoji }}</div>
                <h4 class="font-heading font-bold text-sm text-gray-900">{{ occ.title }}</h4>
                <p class="text-[11px] text-gray-500 mt-1 leading-snug">{{ occ.desc }}</p>
              </div>

              <div class="mt-3.5 pt-2 border-t border-gray-100 flex items-center justify-between text-[10px]">
                <span class="font-semibold text-gray-500">{{ occ.tag }}</span>
                <span
                  class="font-bold uppercase tracking-wider"
                  :class="occasion === occ.title ? 'text-[#f47b20]' : 'text-gray-400'"
                >
                  {{ occasion === occ.title ? 'Selected' : 'Choose' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Date & Guest Range -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2.5 flex items-center gap-1.5">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">2</span>
              <span>Planned Event Date</span>
            </label>
            <input
              v-model="date"
              type="date"
              :min="todayIsoString"
              required
              class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2.5 flex items-center gap-1.5">
              <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">3</span>
              <span>Expected Guest Count</span>
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button
                v-for="g in ['15-25 Guests', '25-50 Guests', '50-100 Guests', '100+ Guests']"
                :key="g"
                type="button"
                @click="guestCount = g"
                :class="[
                  'py-2.5 px-2 rounded-xl text-xs font-bold border transition-all cursor-pointer text-center truncate',
                  guestCount === g
                    ? 'border-[#f47b20] bg-orange-50 text-[#f47b20] ring-2 ring-orange-400/20 font-black'
                    : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
                ]"
              >
                {{ g.replace(' Guests', '') }}
                <span class="block text-[10px] font-normal text-gray-500">Guests</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 3. Catering & Banqueting Packages -->
        <div class="pt-2">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">4</span>
            <span>Select Banqueting Package Tier</span>
          </label>
          <div class="grid gap-3 sm:grid-cols-3">
            <div
              v-for="pkg in packages"
              :key="pkg.name"
              @click="selectedPackage = pkg.name"
              :class="[
                'p-4 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between',
                selectedPackage === pkg.name
                  ? 'border-[#f47b20] bg-orange-50/60 shadow-md ring-2 ring-orange-400/25'
                  : 'border-gray-200 bg-gray-50/40 hover:border-gray-300'
              ]"
            >
              <div>
                <div class="flex items-center justify-between">
                  <span class="font-heading font-black text-sm text-gray-900">{{ pkg.name }}</span>
                  <span class="font-bold text-xs text-[#f47b20]">{{ pkg.price }}</span>
                </div>
                <p class="text-[11px] text-gray-500 mt-1">{{ pkg.desc }}</p>
                <ul class="mt-2.5 space-y-1 text-[11px] text-gray-600">
                  <li v-for="inc in pkg.features" :key="inc" class="flex items-center gap-1.5">
                    <Check :size="12" class="text-emerald-600 shrink-0" />
                    <span>{{ inc }}</span>
                  </li>
                </ul>
              </div>
              <div class="mt-3.5 pt-2 border-t border-gray-200/60 text-right">
                <span
                  class="text-[10px] font-bold uppercase tracking-wider"
                  :class="selectedPackage === pkg.name ? 'text-[#f47b20]' : 'text-gray-400'"
                >
                  {{ selectedPackage === pkg.name ? '● Selected Tier' : 'Choose Tier' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Desired Inclusions & Custom Requirements -->
        <div class="pt-2">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-3 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">5</span>
            <span>Custom Add-ons & Amenities</span>
          </label>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 mb-3.5">
            <div
              v-for="req in popularRequirements"
              :key="req.label"
              @click="toggleRequirement(req.label)"
              :class="[
                'p-2.5 rounded-xl border text-xs font-semibold cursor-pointer transition-all flex items-center justify-between text-center select-none',
                requirements.includes(req.label)
                  ? 'border-emerald-600 bg-emerald-50 text-emerald-900 font-bold ring-1 ring-emerald-500/30'
                  : 'border-gray-200 bg-gray-50 text-gray-700 hover:border-gray-300'
              ]"
            >
              <div class="flex items-center gap-1.5 truncate">
                <span>{{ req.icon }}</span>
                <span class="truncate">{{ req.label }}</span>
              </div>
              <Check v-if="requirements.includes(req.label)" :size="13" class="text-emerald-600 shrink-0 ml-1" />
            </div>
          </div>

          <textarea
            v-model="requirements"
            rows="3"
            placeholder="Additional requirements e.g. Pure Jain / Vegan menu, anniversary photo wall, champagne toast, live acoustic guitarist..."
            class="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-800 focus:border-[#f47b20] focus:bg-white focus:outline-none transition-colors"
          ></textarea>
        </div>

        <!-- 5. Host Contact Details -->
        <div class="border-t border-gray-100 pt-6">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-4 flex items-center gap-1.5">
            <span class="flex h-5 w-5 items-center justify-center rounded-full bg-[#f47b20] text-white text-[10px]">6</span>
            <span>Host & Organizer Details</span>
          </label>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-gray-700 mb-1.5">Host Full Name / Organization</label>
              <input
                v-model="clientName"
                type="text"
                required
                placeholder="Enter organizer / host name"
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
            <Gift :size="18" />
            <span>{{ isSubmitting ? 'Dispatching to Event Director...' : 'Submit Banquet & Party Request' }}</span>
          </button>
          <p class="text-center text-[11px] text-gray-500 mt-2.5">
            ✨ Guaranteed price quote with no hidden venue charges.
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
import {
  Gift,
  Sparkles,
  CheckCircle2,
  Check,
  PhoneCall,
  MessageSquare,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'

const occasion = ref('Birthday Bash')
const guestCount = ref('25-50 Guests')
const date = ref(new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0])
const clientName = ref('')
const phone = ref('')
const selectedPackage = ref('Gold Grandeur')
const requirements = ref('')
const submitted = ref(false)
const isSubmitting = ref(false)
const error = ref('')
const partyRef = ref('SHP-PRT-9021')

const todayIsoString = computed(() => new Date().toISOString().split('T')[0])

const phoneError = computed(() =>
  phone.value && !/^\d{10}$/.test(phone.value)
    ? 'Please enter a valid 10-digit mobile number.'
    : ''
)

const occasions = [
  {
    title: 'Birthday Bash',
    emoji: '🎂',
    desc: 'Custom cake, themed balloon decor, live music & photo setup',
    tag: 'All Ages',
  },
  {
    title: 'Corporate Gala',
    emoji: '💼',
    desc: 'Audio/visual podium, multi-course buffet & cocktail lounge',
    tag: 'Formal Setup',
  },
  {
    title: 'Anniversary & Date',
    emoji: '🥂',
    desc: 'Candlelight dinner, live acoustic music & signature mocktails',
    tag: 'Intimate Banquet',
  },
  {
    title: 'Family Gathering',
    emoji: '🎉',
    desc: 'Spacious private hall, kids zone & custom buffet spread',
    tag: 'Grand Hall',
  },
]

const packages = [
  {
    name: 'Silver Elegance',
    price: '₹799 / guest',
    desc: 'Ideal for informal gatherings & high-tea parties',
    features: ['3 Starters & 2 Main Courses', 'Standard Table Decor', 'Welcome Mocktail Drinks'],
  },
  {
    name: 'Gold Grandeur',
    price: '₹1,199 / guest',
    desc: 'Our most popular all-inclusive banquet package',
    features: ['5 Starters & 4 Main Courses', 'Themed Balloon/Floral Decor', 'Dessert Counter & Cake Service', 'Audio DJ System Included'],
  },
  {
    name: 'Platinum Imperial',
    price: '₹1,699 / guest',
    desc: 'Ultimate luxury with live counters & private chef',
    features: ['Unlimited Multi-Cuisine Buffet', 'Live Chef Tawa & Pasta Stations', 'Dedicated Event Host & Photographer', 'Exclusive Rooftop or VIP Hall'],
  },
]

const popularRequirements = [
  { label: 'Balloon Decor', icon: '🎈' },
  { label: 'Custom Cake', icon: '🍰' },
  { label: 'Live DJ & Sound', icon: '🎵' },
  { label: 'Cocktail Bar', icon: '🍸' },
  { label: 'Photography', icon: '📸' },
  { label: 'Jain Food Spread', icon: '🌱' },
]

function toggleRequirement(req: string) {
  const parts = requirements.value.split(',').map((s) => s.trim()).filter(Boolean)
  if (parts.includes(req)) {
    requirements.value = parts.filter((p) => p !== req).join(', ')
  } else {
    parts.push(req)
    requirements.value = parts.join(', ')
  }
}

function resetPartyForm() {
  submitted.value = false
  error.value = ''
  clientName.value = ''
  phone.value = ''
  requirements.value = ''
}

async function handleSubmit() {
  error.value = ''
  if (!/^\d{10}$/.test(phone.value)) {
    error.value = 'Please enter a valid 10-digit mobile number.'
    return
  }
  isSubmitting.value = true
  try {
    const booking = await restroHandler.reservations.createPartyBooking({
      occasion: occasion.value,
      client: clientName.value,
      phone: phone.value,
      date: date.value,
      guestCount: `${guestCount.value} (${selectedPackage.value})`,
      requirements: requirements.value,
    })
    partyRef.value = booking?.id
      ? `SHP-PRT-${booking.id}`
      : `SHP-PRT-${Math.floor(1000 + Math.random() * 9000)}`
    submitted.value = true
  } catch (err) {
    error.value = getApiErrorMessage(err) || 'We could not submit your party request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e] flex flex-col justify-between selection:bg-[#f47b20]/20 selection:text-[#f47b20]">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 flex-1 w-full">
      <!-- Header Banner -->
      <div class="mb-8 sm:mb-12 text-center max-w-2xl mx-auto">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100/90 border border-orange-200/80 px-3.5 py-1 text-xs font-bold text-[#f47b20] shadow-xs">
          <Percent :size="13" class="animate-pulse" /> Verified Promo Codes & Vouchers
        </span>
        <h1 class="mt-3.5 font-heading text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-gray-900 leading-tight">
          Deals & Dining Offers
        </h1>
        <p class="mt-2.5 text-xs sm:text-sm text-gray-600 leading-relaxed">
          Grab instant discounts on online doorstep delivery, table bookings, and festive banquet feasts.
        </p>
      </div>

      <!-- Filter Tabs -->
      <div class="mb-8 flex items-center justify-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          v-for="cat in categories"
          :key="cat"
          type="button"
          @click="activeCategory = cat"
          :class="[
            'px-4 py-2 rounded-full text-xs font-bold transition-all shrink-0 cursor-pointer',
            activeCategory === cat
              ? 'bg-[#f47b20] text-white shadow-md shadow-orange-500/20'
              : 'bg-white border border-gray-200 text-gray-700 hover:border-gray-300 hover:bg-gray-50'
          ]"
        >
          {{ cat }}
        </button>
      </div>

      <!-- Copy Toast Notification -->
      <div
        v-if="toastMessage"
        class="fixed bottom-6 right-6 z-50 rounded-2xl bg-gray-900 text-white px-5 py-3 text-xs font-bold shadow-2xl flex items-center gap-2.5 animate-bounce"
      >
        <CheckCircle2 :size="16" class="text-emerald-400" />
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="isLoading" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="n in 6"
          :key="n"
          class="rounded-3xl border border-gray-200/90 bg-white p-6 shadow-xs animate-pulse space-y-4"
        >
          <div class="flex items-center justify-between">
            <div class="h-5 w-20 bg-gray-200 rounded-full"></div>
            <div class="h-4 w-16 bg-gray-100 rounded"></div>
          </div>
          <div class="h-13 w-13 rounded-2xl bg-gray-200"></div>
          <div class="h-5 bg-gray-200 rounded w-3/4"></div>
          <div class="h-7 bg-gray-200 rounded w-1/2"></div>
          <div class="border-t border-dashed border-gray-200 pt-5">
            <div class="h-10 bg-gray-100 rounded-xl"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        class="text-center py-16 bg-white rounded-3xl border border-rose-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center text-3xl mx-auto mb-4 border border-rose-100">
          ⚠️
        </div>
        <h3 class="text-base sm:text-lg font-black text-gray-900 font-heading">Unable to Load Offers</h3>
        <p class="text-xs sm:text-sm text-gray-500 mt-1.5 max-w-sm mx-auto leading-relaxed">{{ error }}</p>
        <button
          @click="loadOffers"
          class="mt-5 text-xs font-bold text-white bg-gray-900 px-5 py-2.5 rounded-xl hover:bg-[#f47b20] transition-colors shadow-sm cursor-pointer active:scale-95"
        >
          Retry
        </button>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="offers.length === 0"
        class="text-center py-16 bg-white rounded-3xl border border-gray-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-orange-50 text-[#f47b20] flex items-center justify-center text-3xl mx-auto mb-4 border border-orange-100">
          🎁
        </div>
        <h3 class="text-base sm:text-lg font-black text-gray-900 font-heading">No Active Offers</h3>
        <p class="text-xs sm:text-sm text-gray-500 mt-1.5 max-w-sm mx-auto leading-relaxed">
          There are no promotions running right now. Check back soon for fresh deals and vouchers.
        </p>
      </div>

      <!-- Filtered Empty State -->
      <div
        v-else-if="filteredOffers.length === 0"
        class="text-center py-16 bg-white rounded-3xl border border-gray-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-orange-50 text-[#f47b20] flex items-center justify-center text-3xl mx-auto mb-4 border border-orange-100">
          🎁
        </div>
        <h3 class="text-base sm:text-lg font-black text-gray-900 font-heading">No Offers in This Category</h3>
        <p class="text-xs sm:text-sm text-gray-500 mt-1.5 max-w-sm mx-auto leading-relaxed">
          Try selecting a different category to view available promotions.
        </p>
      </div>

      <!-- Offers Grid -->
      <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="offer in filteredOffers"
          :key="offer.code"
          class="relative overflow-hidden rounded-3xl border border-gray-200/90 bg-white p-6 shadow-xs hover:shadow-xl hover:border-orange-200 transition-all duration-300 flex flex-col justify-between group"
        >
          <!-- Scalloped ticket punch cutouts on sides for realistic voucher look -->
          <div class="absolute -left-3 top-1/2 -translate-y-1/2 h-6 w-6 rounded-full bg-[#fffdf9] border-r border-gray-200"></div>
          <div class="absolute -right-3 top-1/2 -translate-y-1/2 h-6 w-6 rounded-full bg-[#fffdf9] border-l border-gray-200"></div>

          <!-- Top Tag Badge -->
          <div class="flex items-center justify-between gap-2 mb-4">
            <span
              :class="[
                'rounded-full px-3 py-1 text-[10px] font-black uppercase tracking-wider shadow-xs',
                offer.badge_color || 'bg-orange-500 text-white'
              ]"
            >
              {{ offer.tag }}
            </span>

            <span v-if="offer.validity" class="text-[11px] font-bold text-gray-400 flex items-center gap-1">
              <Clock :size="12" /> {{ offer.validity }}
            </span>
          </div>

          <!-- Coupon Header & Info -->
          <div>
            <div class="mb-3 flex h-13 w-13 items-center justify-center rounded-2xl bg-orange-50 text-[#f47b20] group-hover:scale-110 transition-transform">
              <Gift :size="26" />
            </div>

            <h3 class="font-heading text-lg font-black text-gray-900 leading-snug">{{ offer.title }}</h3>
            <p class="text-2xl sm:text-3xl font-black text-[#f47b20] mt-1 font-heading tracking-tight">
              {{ offer.discount }}
            </p>
            <p class="text-xs text-gray-500 mt-1 flex items-center gap-1">
              <Sparkles :size="12" class="text-amber-500" />
              <span>{{ offer.min_spend }}</span>
            </p>
          </div>

          <!-- Ticket Bottom Border / Action Bar -->
          <div class="mt-6 border-t border-dashed border-gray-200 pt-5 space-y-3">
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-1.5 font-mono text-xs font-black tracking-widest text-gray-800 bg-gray-100/90 px-3.5 py-2 rounded-xl border border-dashed border-gray-300">
                <Tag :size="13" class="text-gray-400" />
                <span>{{ offer.code }}</span>
              </div>

              <button
                @click="handleCopy(offer.code)"
                type="button"
                class="flex items-center gap-1.5 rounded-xl bg-gray-900 px-3.5 py-2 text-xs font-bold text-white hover:bg-[#f47b20] transition-colors cursor-pointer active:scale-95"
              >
                <Check v-if="copiedCode === offer.code" :size="14" class="text-emerald-400" />
                <Copy v-else :size="14" />
                <span>{{ copiedCode === offer.code ? 'Copied!' : 'Copy Code' }}</span>
              </button>
            </div>

            <button
              type="button"
              @click="applyAndOrder(offer.code)"
              class="w-full text-center text-xs font-bold text-[#f47b20] bg-orange-50 hover:bg-orange-100/80 py-2.5 rounded-xl transition-colors cursor-pointer flex items-center justify-center gap-1"
            >
              <span>Apply & Order Online</span>
              <ArrowRight :size="13" />
            </button>
          </div>
        </div>
      </div>

      <!-- Terms & FAQ Banner -->
      <div class="mt-12 rounded-3xl bg-gradient-to-r from-gray-950 via-gray-900 to-gray-800 p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-6 relative z-10">
          <div class="space-y-1.5 text-center sm:text-left">
            <span class="text-[10px] uppercase tracking-widest font-black text-[#f47b20]">Promotion Guidelines</span>
            <h4 class="font-heading font-black text-lg sm:text-xl">Terms & Conditions of Offers</h4>
            <p class="text-xs text-gray-300 max-w-xl leading-relaxed">
              One promo code per order. Codes are valid across all food categories and automatically applied during checkout. Cannot be combined with external table booking deals.
            </p>
          </div>
          <RouterLink
            to="/delivery"
            class="orange-button px-7 py-3.5 rounded-xl font-bold text-xs shrink-0 shadow-lg"
          >
            Start Ordering Now
          </RouterLink>
        </div>
      </div>
    </main>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import {
  Percent,
  Gift,
  Copy,
  Check,
  CheckCircle2,
  Clock,
  Sparkles,
  Tag,
  ArrowRight,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler, type OfferData } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'

const router = useRouter()
const copiedCode = ref<string | null>(null)
const toastMessage = ref<string | null>(null)
const activeCategory = ref('All Offers')

const offers = ref<OfferData[]>([])
const isLoading = ref(true)
const error = ref('')

// Category tabs are derived from real offer data, never fabricated.
const categories = computed(() => {
  const dynamic = Array.from(
    new Set(offers.value.map((o) => o.category).filter((c): c is string => Boolean(c)))
  )
  return ['All Offers', ...dynamic]
})

const filteredOffers = computed(() => {
  if (activeCategory.value === 'All Offers') return offers.value
  return offers.value.filter((o) => o.category === activeCategory.value)
})

async function loadOffers() {
  isLoading.value = true
  error.value = ''
  try {
    const data = await restroHandler.offers.list()
    offers.value = Array.isArray(data) ? data : []
  } catch (err) {
    error.value = getApiErrorMessage(err)
    offers.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(loadOffers)

function handleCopy(code: string) {
  navigator.clipboard.writeText(code)
  copiedCode.value = code
  toastMessage.value = `Coupon code "${code}" copied to clipboard!`
  
  setTimeout(() => {
    copiedCode.value = null
  }, 2500)

  setTimeout(() => {
    toastMessage.value = null
  }, 3500)
}

function applyAndOrder(code: string) {
  handleCopy(code)
  try {
    localStorage.setItem('active_coupon_code', code)
  } catch {}
  router.push('/delivery')
}
</script>

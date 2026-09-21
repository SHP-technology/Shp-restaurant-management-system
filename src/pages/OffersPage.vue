<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, Percent, Gift, Copy, Check } from 'lucide-vue-next'
import { restroHandler, type OfferData } from '../services/api'

const copiedCode = ref<string | null>(null)
const offers = ref<OfferData[]>([
  {
    title: 'Weekend Special Offer',
    discount: 'Flat 20% OFF',
    min_spend: 'On all orders above ₹499',
    code: 'SHP20',
    tag: 'HOT DEAL',
    badge_color: 'bg-rose-500 text-white',
  },
  {
    title: 'Welcome First Order',
    discount: '15% OFF',
    min_spend: 'On your very first order',
    code: 'WELCOME15',
    tag: 'NEW USER',
    badge_color: 'bg-[#f47b20] text-white',
  },
  {
    title: 'Sweet Delight',
    discount: 'Free Dessert',
    min_spend: 'On orders above ₹699',
    code: 'DESSERT',
    tag: 'SPECIAL',
    badge_color: 'bg-emerald-600 text-white',
  },
])

onMounted(async () => {
  try {
    const data = await restroHandler.offers.list()
    if (Array.isArray(data) && data.length > 0) {
      offers.value = data
    }
  } catch {}
})

function handleCopy(code: string) {
  navigator.clipboard.writeText(code)
  copiedCode.value = code
  setTimeout(() => {
    copiedCode.value = null
  }, 2000)
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
        <span class="font-heading text-lg font-bold text-gray-900">Offers & Discounts</span>
        <div class="w-16" />
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-6 py-12">
      <div class="mb-10 text-center">
        <span class="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
          <Percent :size="14" /> Exclusive Deals
        </span>
        <h1 class="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
          Save Big on Gourmet Meals
        </h1>
        <p class="mt-2 text-xs sm:text-sm text-gray-500">
          Apply discount codes at checkout for instant savings on dine-in & doorstep delivery.
        </p>
      </div>

      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="offer in offers"
          :key="offer.code"
          class="relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-md"
        >
          <span :class="['absolute top-4 right-4 rounded-full px-3 py-1 text-[10px] font-bold', offer.badge_color || 'bg-[#f47b20] text-white']">
            {{ offer.tag }}
          </span>

          <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-[#f47b20]">
            <Gift :size="24" />
          </div>

          <h3 class="font-heading text-lg font-bold text-gray-900">{{ offer.title }}</h3>
          <p class="text-2xl font-black text-[#f47b20] mt-1">{{ offer.discount }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ offer.min_spend }}</p>

          <div class="mt-6 flex items-center justify-between border-t border-dashed border-gray-200 pt-4">
            <span class="font-mono text-xs font-bold tracking-wider text-gray-800 bg-gray-100 px-3 py-1.5 rounded border border-gray-300">
              {{ offer.code }}
            </span>

            <button
              @click="handleCopy(offer.code)"
              class="flex items-center gap-1.5 rounded-md bg-[#f47b20] px-3.5 py-1.5 text-xs font-bold text-white transition hover:bg-[#d9630f]"
            >
              <template v-if="copiedCode === offer.code">
                <Check :size="14" /> Copied
              </template>
              <template v-else>
                <Copy :size="14" /> Copy Code
              </template>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

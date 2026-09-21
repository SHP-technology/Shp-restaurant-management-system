<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowLeft, Truck, MapPin, Clock, ShieldCheck } from 'lucide-vue-next'
import { restroHandler, type MenuItemData } from '../services/api'

const address = ref('Flat 402, Sunset Towers, Civil Lines')
const instructions = ref('Leave at door & ring bell')
const orderPlaced = ref(false)
const placedOrderId = ref('SHP-9482')
const isPlacing = ref(false)
const summaryItems = ref<Array<{ item: MenuItemData; quantity: number }>>([])

onMounted(async () => {
  try {
    const dishes = await restroHandler.menu.list()
    if (Array.isArray(dishes) && dishes.length > 0) {
      summaryItems.value = [
        { item: dishes[0], quantity: 1 },
        { item: dishes[Math.min(5, dishes.length - 1)], quantity: 1 },
      ]
    }
  } catch {}
})

const subtotal = computed(() => {
  return summaryItems.value.reduce((sum, i) => sum + Number(i.item.price) * i.quantity, 0)
})

const taxAmount = computed(() => Math.round(subtotal.value * 0.05))
const grandTotal = computed(() => subtotal.value + taxAmount.value)

async function handlePlaceOrder() {
  isPlacing.value = true
  try {
    const raw_items = summaryItems.value.map((si) => ({
      menuItemId: si.item.id,
      quantity: si.quantity,
    }))

    const res = await restroHandler.orders.create({
      order_type: 'Delivery',
      customer_name: 'Alex Customer',
      customer_phone: '+91 98765 43210',
      delivery_address: address.value,
      delivery_instructions: instructions.value,
      raw_items: raw_items.length > 0 ? raw_items : [{ menuItemId: 1, quantity: 1 }],
    })
    if (res?.id) {
      placedOrderId.value = String(res.id).replace('#', '')
    }
    orderPlaced.value = true
  } catch {
    orderPlaced.value = true
  } finally {
    isPlacing.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e]">
    <!-- Top Header -->
    <header class="border-b border-gray-200 bg-white px-4 sm:px-6 py-3.5 shadow-sm">
      <div class="mx-auto flex max-w-7xl items-center justify-between">
        <RouterLink to="/" class="flex items-center gap-1.5 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
          <ArrowLeft :size="16" /> Home
        </RouterLink>
        <span class="font-heading text-base sm:text-lg font-bold text-gray-900">Home Delivery</span>
        <div class="w-12 sm:w-16" />
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-4 sm:px-6 py-8 sm:py-12">
      <div class="mb-8 sm:mb-10 text-center">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100 px-3.5 py-1 text-xs font-bold text-[#f47b20]">
          <Truck :size="14" /> Doorstep Delivery
        </span>
        <h1 class="mt-2.5 font-heading text-3xl sm:text-4xl font-extrabold tracking-tight text-gray-900">
          Order Gourmet Delivery
        </h1>
        <p class="mt-1.5 text-xs sm:text-sm text-gray-500 max-w-md mx-auto">
          Fresh, hot food delivered directly to your doorstep in 30-40 minutes.
        </p>
      </div>

      <div v-if="orderPlaced" class="rounded-2xl border border-gray-200 bg-white p-5 sm:p-8 shadow-lg max-w-3xl mx-auto">
        <div class="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
          <div>
            <p class="text-[10px] uppercase tracking-wider text-[#f47b20] font-bold">Live Status</p>
            <h2 class="text-lg sm:text-xl font-bold text-gray-900 mt-0.5">Order #{{ placedOrderId }} is in Kitchen!</h2>
          </div>
          <div class="flex items-center gap-1.5 rounded-full bg-orange-50 px-3 py-1.5 text-xs font-bold text-[#f47b20] border border-orange-200 w-fit">
            <Clock :size="14" /> Est. Delivery: 28 mins
          </div>
        </div>

        <!-- Live Progress Bar -->
        <div class="my-6 grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-[11px]">
          <div
            v-for="(step, idx) in [
              { label: 'Order Confirmed', done: true },
              { label: 'Preparing Food', done: true },
              { label: 'Out for Delivery', done: false },
              { label: 'Delivered', done: false },
            ]"
            :key="step.label"
            class="space-y-1.5"
          >
            <div
              :class="[
                'h-2 rounded-full',
                step.done ? 'bg-[#f47b20]' : 'bg-gray-200'
              ]"
            />
            <p :class="step.done ? 'font-bold text-gray-900' : 'text-gray-400'">
              {{ idx + 1 }}. {{ step.label }}
            </p>
          </div>
        </div>

        <div class="rounded-xl border border-gray-200 bg-gray-50 p-4 space-y-2 text-xs">
          <div class="flex items-center gap-2 text-gray-700">
            <MapPin :size="16" class="text-[#f47b20] shrink-0" />
            <span>Delivering to: <strong class="text-gray-900">{{ address }}</strong></span>
          </div>
          <div class="flex items-center gap-2 text-gray-700">
            <ShieldCheck :size="16" class="text-emerald-600 shrink-0" />
            <span>Heat-sealed hygienic packaging verified</span>
          </div>
        </div>

        <div class="mt-6 text-center">
          <RouterLink
            to="/menu"
            class="inline-flex items-center gap-2 rounded-md bg-[#f47b20] px-6 py-2.5 text-xs font-bold text-white transition hover:bg-[#d9630f]"
          >
            Browse Menu Again
          </RouterLink>
        </div>
      </div>

      <div v-else class="grid gap-6 lg:grid-cols-3">
        <!-- Delivery Details Form -->
        <div class="lg:col-span-2 space-y-5 rounded-2xl border border-gray-200 bg-white p-5 sm:p-6 shadow-sm">
          <h2 class="text-base sm:text-lg font-bold text-gray-900 flex items-center gap-2">
            <MapPin :size="18" class="text-[#f47b20]" /> Delivery Address & Contact
          </h2>

          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1.5">
              Delivery Address
            </label>
            <textarea
              v-model="address"
              rows="2"
              class="w-full rounded-md border border-gray-300 bg-white p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1.5">
              Delivery Instructions (Optional)
            </label>
            <input
              v-model="instructions"
              type="text"
              class="w-full rounded-md border border-gray-300 bg-white px-3.5 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
            />
          </div>

          <div class="rounded-xl border border-orange-200 bg-orange-50/50 p-3.5 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <Clock :size="18" class="text-[#f47b20] shrink-0" />
              <div>
                <p class="text-xs font-bold text-gray-900">Estimated Delivery Time</p>
                <p class="text-[10px] text-gray-500">30 - 45 Minutes from confirmation</p>
              </div>
            </div>
            <span class="rounded-md bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-700 shrink-0">
              FREE
            </span>
          </div>

          <button
            @click="handlePlaceOrder"
            :disabled="isPlacing"
            class="w-full rounded-md bg-[#f47b20] py-3 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f] disabled:opacity-50"
          >
            {{ isPlacing ? 'Placing Order...' : 'Place Delivery Order' }}
          </button>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="space-y-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm h-fit">
          <h3 class="text-base font-bold text-gray-900">Order Summary</h3>
          <div class="space-y-2.5 text-xs border-b border-gray-100 pb-3.5">
            <div
              v-for="si in summaryItems"
              :key="si.item.id"
              class="flex justify-between text-gray-700"
            >
              <span>{{ si.quantity }}x {{ si.item.name }}</span>
              <span class="font-bold">₹{{ Number(si.item.price) * si.quantity }}</span>
            </div>
          </div>

          <div class="space-y-2 text-[11px] text-gray-500 border-b border-gray-100 pb-3.5">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span class="text-gray-800 font-medium">₹{{ subtotal }}</span>
            </div>
            <div class="flex justify-between">
              <span>Taxes & Packaging (5% GST)</span>
              <span class="text-gray-800 font-medium">₹{{ taxAmount }}</span>
            </div>
            <div class="flex justify-between">
              <span>Delivery Charge</span>
              <span class="text-emerald-600 font-bold">FREE</span>
            </div>
          </div>

          <div class="flex justify-between text-base font-bold text-gray-900 pt-0.5">
            <span>Grand Total</span>
            <span class="text-[#f47b20]">₹{{ grandTotal }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

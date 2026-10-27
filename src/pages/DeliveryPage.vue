<template>
  <div class="min-h-screen bg-[#faf8f5] text-[#1a1f1c] flex flex-col justify-between selection:bg-orange-500 selection:text-white">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 flex-1 w-full">
      <!-- Title Header -->
      <div class="mb-8 sm:mb-10 text-center">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-orange-100/80 border border-orange-200 px-4 py-1.5 text-xs font-bold text-[#ea580c] shadow-xs">
          <Truck :size="14" /> 30-Min Fast Gourmet Delivery & Online Payment
        </span>
        <h1 class="mt-3 font-heading text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-slate-900">
          Doorstep Delivery & Razorpay Checkout
        </h1>
        <p class="mt-2 text-xs sm:text-sm text-slate-500 max-w-md mx-auto">
          Pay securely via UPI, Cards, or Netbanking powered by Razorpay.
        </p>
      </div>

      <!-- Placed Order Live Status Tracker -->
      <div v-if="orderPlaced" class="rounded-3xl border border-slate-200/90 bg-white p-6 sm:p-10 shadow-xl max-w-3xl mx-auto">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
          <div>
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-700 text-xs font-bold px-3 py-1 rounded-full border border-emerald-200">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Order Confirmed
              </span>
              <span v-if="paymentMethod === 'Razorpay' && paymentId" class="inline-flex items-center gap-1 bg-blue-50 text-blue-700 text-xs font-bold px-3 py-1 rounded-full border border-blue-200">
                <span>💳 Paid via Razorpay</span>
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-slate-900 mt-2 font-heading">
              Order #{{ placedOrderId }} is Cooking in Kitchen!
            </h2>
            <p class="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
              <MapPin :size="13" class="text-orange-500" /> {{ address }}
            </p>
            <p v-if="paymentId" class="text-[11px] text-slate-400 font-mono mt-1">
              Razorpay Ref: {{ paymentId }}
            </p>
          </div>
          <div class="flex items-center gap-2 rounded-2xl bg-orange-50 px-4 py-2 text-xs font-bold text-orange-700 border border-orange-200/80 w-fit">
            <Clock :size="16" />
            <span>Est. Delivery: 25-30 mins</span>
          </div>
        </div>

        <!-- 4-Stage Visual Progress Bar -->
        <div class="my-8 grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
          <div
            v-for="(stage, idx) in trackerStages"
            :key="stage.name"
            :class="[
              'rounded-2xl p-4 border transition-all flex flex-col items-center justify-center gap-2',
              idx <= currentStageIndex
                ? 'border-orange-300 bg-orange-50/70 text-[#ea580c] font-bold shadow-xs'
                : 'border-slate-100 bg-slate-50 text-slate-400'
            ]"
          >
            <div class="text-2xl">{{ stage.emoji }}</div>
            <div class="text-xs font-heading">{{ stage.name }}</div>
            <div v-if="idx === currentStageIndex" class="text-[10px] text-orange-600 font-semibold animate-pulse">
              In Progress
            </div>
            <div v-else-if="idx < currentStageIndex" class="text-[10px] text-emerald-600 font-bold">
              ✓ Done
            </div>
          </div>
        </div>

        <!-- Ordered Items Summary Box -->
        <div class="rounded-2xl bg-slate-50 p-5 border border-slate-200/80 mb-6">
          <div class="text-xs font-bold text-slate-600 uppercase tracking-wider mb-3">Dishes in this Delivery</div>
          <div class="space-y-2">
            <div
              v-for="si in summaryItems"
              :key="si.item.id"
              class="flex items-center justify-between text-xs sm:text-sm text-slate-800"
            >
              <div class="flex items-center gap-2">
                <span class="font-bold text-orange-600">{{ si.quantity }}x</span>
                <span class="font-semibold">{{ si.item.name }}</span>
              </div>
              <span class="font-bold">₹{{ Number(si.item.price) * si.quantity }}</span>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between font-bold text-sm text-slate-900">
            <span>Grand Total (Paid)</span>
            <span class="text-orange-600 text-lg font-heading font-black">₹{{ grandTotal }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
          <RouterLink
            to="/menu"
            class="w-full sm:w-auto orange-button px-6 py-3.5 rounded-2xl font-bold text-xs text-center shadow-md"
          >
            Browse More Menu
          </RouterLink>
          <button
            @click="orderPlaced = false"
            class="w-full sm:w-auto bg-slate-100 hover:bg-slate-200 text-slate-700 px-6 py-3.5 rounded-2xl font-bold text-xs transition-colors cursor-pointer"
          >
            Place New Delivery Order
          </button>
        </div>
      </div>

      <!-- Delivery Checkout Form & Cart -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Delivery Details Form -->
        <div class="lg:col-span-7 space-y-6">
          <div class="rounded-3xl border border-slate-200/90 bg-white p-6 sm:p-8 shadow-xs space-y-6">
            <h2 class="font-heading text-xl font-bold text-slate-900 flex items-center gap-2">
              <MapPin class="text-orange-600" :size="20" />
              <span>1. Delivery Address</span>
            </h2>

            <div class="space-y-4">
              <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                  Full Street Address, House/Flat & Area
                </label>
                <input
                  v-model="address"
                  type="text"
                  required
                  placeholder="Enter flat/house number, street address & landmark"
                  class="w-full rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-3 text-sm text-slate-900 focus:border-orange-500 focus:bg-white focus:outline-none focus:ring-3 focus:ring-orange-500/10 transition-all"
                />
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                    Your Name
                  </label>
                  <input
                    v-model="customerName"
                    type="text"
                    required
                    placeholder="Enter your full name"
                    class="w-full rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-3 text-sm text-slate-900 focus:border-orange-500 focus:bg-white focus:outline-none focus:ring-3 focus:ring-orange-500/10 transition-all"
                  />
                </div>
                <div>
                  <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                    Phone Number
                  </label>
                  <input
                    v-model="customerPhone"
                    type="tel"
                    required
                    placeholder="Enter 10-digit mobile number"
                    class="w-full rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-3 text-sm text-slate-900 focus:border-orange-500 focus:bg-white focus:outline-none focus:ring-3 focus:ring-orange-500/10 transition-all"
                  />
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5">
                  Delivery Notes & Instructions (Optional)
                </label>
                <input
                  v-model="instructions"
                  type="text"
                  placeholder="e.g. Ring doorbell, leave at door, call on arrival"
                  class="w-full rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-3 text-sm text-slate-900 focus:border-orange-500 focus:bg-white focus:outline-none focus:ring-3 focus:ring-orange-500/10 transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Payment Method Selection (Razorpay vs COD) -->
          <div class="rounded-3xl border border-slate-200/90 bg-white p-6 sm:p-8 shadow-xs space-y-4">
            <h2 class="font-heading text-xl font-bold text-slate-900 flex items-center gap-2">
              <CreditCard class="text-orange-600" :size="20" />
              <span>2. Payment Method</span>
            </h2>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Razorpay Option -->
              <div
                @click="paymentMethod = 'Razorpay'"
                :class="[
                  'p-4 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between',
                  paymentMethod === 'Razorpay'
                    ? 'border-orange-500 bg-orange-50/50 shadow-xs ring-2 ring-orange-500/20'
                    : 'border-slate-200 hover:border-slate-300 bg-white'
                ]"
              >
                <div class="flex items-center justify-between">
                  <div class="font-bold text-sm text-slate-900 flex items-center gap-2">
                    <span class="text-lg">⚡</span>
                    <span>Razorpay Online</span>
                  </div>
                  <span class="text-[10px] font-extrabold bg-blue-600 text-white px-2 py-0.5 rounded-full">
                    UPI / Cards
                  </span>
                </div>
                <p class="text-[11px] text-slate-500 mt-2">
                  Instant payment via Google Pay, PhonePe, Paytm, UPI QR, Credit/Debit Cards & Netbanking.
                </p>
                <span
                  class="mt-3 text-[10px] font-bold uppercase tracking-wider"
                  :class="paymentMethod === 'Razorpay' ? 'text-orange-600' : 'text-slate-400'"
                >
                  {{ paymentMethod === 'Razorpay' ? '● Selected (Fast)' : 'Select' }}
                </span>
              </div>

              <!-- COD Option -->
              <div
                @click="paymentMethod = 'COD'"
                :class="[
                  'p-4 rounded-2xl border cursor-pointer transition-all flex flex-col justify-between',
                  paymentMethod === 'COD'
                    ? 'border-orange-500 bg-orange-50/50 shadow-xs ring-2 ring-orange-500/20'
                    : 'border-slate-200 hover:border-slate-300 bg-white'
                ]"
              >
                <div class="flex items-center justify-between">
                  <div class="font-bold text-sm text-slate-900 flex items-center gap-2">
                    <span class="text-lg">💵</span>
                    <span>Cash on Delivery</span>
                  </div>
                  <span class="text-[10px] font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-full">
                    Pay at Door
                  </span>
                </div>
                <p class="text-[11px] text-slate-500 mt-2">
                  Pay with exact cash or scan rider's QR upon food arrival at your doorstep.
                </p>
                <span
                  class="mt-3 text-[10px] font-bold uppercase tracking-wider"
                  :class="paymentMethod === 'COD' ? 'text-orange-600' : 'text-slate-400'"
                >
                  {{ paymentMethod === 'COD' ? '● Selected' : 'Select' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Promo Code Card -->
          <div class="rounded-3xl border border-slate-200/90 bg-white p-6 shadow-xs">
            <h3 class="font-heading text-base font-bold text-slate-900 mb-3 flex items-center gap-2">
              <span>🎟️</span>
              <span>Apply Discount Coupon</span>
            </h3>
            <div class="flex gap-2">
              <input
                v-model="couponCode"
                type="text"
                placeholder="Try SHP20 or WELCOME15"
                class="flex-1 rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-2.5 text-xs font-mono font-bold uppercase text-slate-900 focus:border-orange-500 focus:bg-white focus:outline-none"
              />
              <button
                @click="applyCoupon"
                class="rounded-2xl bg-slate-900 px-5 py-2.5 text-xs font-bold text-white hover:bg-orange-600 transition-colors cursor-pointer"
              >
                Apply
              </button>
            </div>
            <p v-if="appliedDiscount > 0" class="text-xs text-emerald-600 font-bold mt-2 flex items-center gap-1">
              ✓ Coupon applied! Saved ₹{{ appliedDiscount }}
            </p>
            <p v-else-if="couponError" class="text-xs text-rose-600 font-bold mt-2 flex items-center gap-1">
              {{ couponError }}
            </p>
          </div>
        </div>

        <!-- Order Summary & Checkout Sidebar -->
        <div class="lg:col-span-5 space-y-6">
          <div class="rounded-3xl border border-slate-200/90 bg-white p-6 sm:p-8 shadow-xs space-y-6">
            <h2 class="font-heading text-xl font-bold text-slate-900 flex items-center justify-between">
              <span>Order Basket</span>
              <RouterLink to="/menu" class="text-xs font-bold text-orange-600 hover:underline">
                + Add Items
              </RouterLink>
            </h2>

            <div v-if="summaryItems.length === 0" class="py-8 text-center space-y-2">
              <ShoppingBag :size="32" class="mx-auto text-slate-300" />
              <p class="text-xs font-semibold text-slate-500">Your basket is currently empty</p>
              <RouterLink to="/menu" class="inline-block text-xs font-bold text-orange-600 hover:underline">
                Explore Menu & Add Dishes →
              </RouterLink>
            </div>

            <div v-else class="divide-y divide-slate-100">
              <div
                v-for="si in summaryItems"
                :key="si.item.id"
                class="py-3 flex items-center justify-between gap-3"
              >
                <div class="flex items-center gap-3">
                  <img
                    :src="si.item.image || 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=150&q=80'"
                    :alt="si.item.name"
                    class="w-12 h-12 rounded-2xl object-cover shadow-2xs"
                  />
                  <div>
                    <h4 class="text-xs sm:text-sm font-bold text-slate-900">{{ si.item.name }}</h4>
                    <span class="text-xs text-orange-600 font-bold">₹{{ si.item.price }}</span>
                  </div>
                </div>

                <!-- Stepper -->
                <div class="flex items-center gap-2 bg-slate-100 rounded-xl px-2 py-1">
                  <button
                    @click="decrementItem(si.item.id)"
                    class="w-6 h-6 rounded-lg text-slate-600 hover:text-black font-bold flex items-center justify-center text-xs cursor-pointer"
                  >
                    -
                  </button>
                  <span class="text-xs font-bold text-slate-900 min-w-4 text-center">{{ si.quantity }}</span>
                  <button
                    @click="incrementItem(si.item.id)"
                    class="w-6 h-6 rounded-lg text-slate-600 hover:text-black font-bold flex items-center justify-center text-xs cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            <!-- Price Breakdown -->
            <div class="border-t border-slate-100 pt-4 space-y-2 text-xs text-slate-600">
              <div class="flex justify-between">
                <span>Subtotal</span>
                <span class="font-bold text-slate-900">₹{{ subtotal }}</span>
              </div>
              <div class="flex justify-between">
                <span>GST (5%)</span>
                <span class="font-bold text-slate-900">₹{{ taxAmount }}</span>
              </div>
              <div class="flex justify-between">
                <span>Doorstep Delivery</span>
                <span class="font-bold text-emerald-600">FREE</span>
              </div>
              <div v-if="appliedDiscount > 0" class="flex justify-between text-emerald-600 font-bold">
                <span>Coupon Discount</span>
                <span>- ₹{{ appliedDiscount }}</span>
              </div>
              <div class="border-t border-slate-200 pt-3 flex justify-between text-lg font-black text-slate-900 font-heading">
                <span>Total Amount</span>
                <span class="text-orange-600 font-black">₹{{ grandTotal }}</span>
              </div>
            </div>

            <div v-if="paymentError" class="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 font-semibold">
              {{ paymentError }}
            </div>

            <!-- Place Order / Razorpay Pay Button -->
            <button
              @click="handlePlaceOrder"
              :disabled="isPlacing || summaryItems.length === 0"
              class="w-full orange-button py-4 rounded-2xl font-bold text-sm shadow-lg shadow-orange-500/25 flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer active:scale-98"
            >
              <CreditCard v-if="paymentMethod === 'Razorpay'" :size="18" />
              <Truck v-else :size="18" />
              <span>
                {{
                  isPlacing
                    ? 'Processing Payment...'
                    : paymentMethod === 'Razorpay'
                    ? `Pay ₹${grandTotal} with Razorpay ⚡`
                    : `Place Order with COD (₹${grandTotal})`
                }}
              </span>
            </button>

            <div class="flex items-center justify-center gap-2 text-[11px] text-slate-400">
              <ShieldCheck :size="14" class="text-emerald-500" />
              <span>256-Bit SSL Encrypted Razorpay Gateway</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Truck, MapPin, Clock, ShieldCheck, CreditCard, ShoppingBag } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler, type MenuItemData } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'
import { openRazorpayCheckout } from '../lib/razorpay'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

const address = ref(cartStore.deliveryAddress || '')
const customerName = ref(cartStore.customerName || '')
const customerPhone = ref(cartStore.customerPhone || '')
const instructions = ref(cartStore.deliveryInstructions || '')
const couponCode = ref(cartStore.couponCode || '')
const appliedDiscount = ref(cartStore.couponDiscount || 0)
const couponError = ref<string | null>(null)
const paymentMethod = ref<'Razorpay' | 'COD'>('Razorpay')
const paymentId = ref<string | null>(null)
const paymentError = ref<string | null>(null)

const orderPlaced = ref(false)
const placedOrderId = ref('SHP-9482')
const isPlacing = ref(false)
const currentStageIndex = ref(1)

const trackerStages = [
  { name: 'Order Confirmed', emoji: '📝' },
  { name: 'Kitchen Cooking', emoji: '🍳' },
  { name: 'Out for Delivery', emoji: '🛵' },
  { name: 'Delivered', emoji: '🏠' },
]

const summaryItems = ref<Array<{ item: MenuItemData; quantity: number }>>([])

onMounted(() => {
  // Mirror the live cart; if it is empty the basket stays empty (no injected default item).
  summaryItems.value = cartStore.items.map((ci) => ({ item: ci.item, quantity: ci.quantity }))
})

function incrementItem(id: number | string) {
  const target = summaryItems.value.find((i) => i.item.id === id)
  if (target) {
    target.quantity += 1
    cartStore.addItem(target.item)
  }
}

function decrementItem(id: number | string) {
  const idx = summaryItems.value.findIndex((i) => i.item.id === id)
  if (idx !== -1) {
    if (summaryItems.value[idx].quantity === 1) {
      cartStore.removeItem(id)
      summaryItems.value.splice(idx, 1)
    } else {
      summaryItems.value[idx].quantity -= 1
      cartStore.decrementItem(id)
    }
  }
}

// Only explicitly recognized codes earn a discount; anything else is rejected.
const KNOWN_COUPONS: Record<string, number> = {
  SHP20: 0.2,
  WELCOME15: 0.15,
}

function applyCoupon() {
  const code = couponCode.value.trim().toUpperCase()
  couponError.value = null

  if (!code) {
    appliedDiscount.value = 0
    couponError.value = 'Please enter a coupon code.'
    return
  }

  const rate = KNOWN_COUPONS[code]
  if (rate === undefined) {
    appliedDiscount.value = 0
    couponError.value = `"${code}" is not a valid coupon.`
    return
  }

  appliedDiscount.value = Math.round(subtotal.value * rate)
}

const subtotal = computed(() => {
  return summaryItems.value.reduce((sum, i) => sum + Number(i.item.price) * i.quantity, 0)
})

const taxAmount = computed(() => Math.round(subtotal.value * 0.05))
const grandTotal = computed(() => Math.max(0, subtotal.value + taxAmount.value - appliedDiscount.value))

// Marks the order confirmed and clears the cart. Called ONLY after a successful
// order (COD) or a fully verified Razorpay payment.
function finalizeOrder() {
  orderPlaced.value = true
  cartStore.clearCart()
}

async function handlePlaceOrder() {
  // Never place an order with an empty basket.
  if (summaryItems.value.length === 0) {
    paymentError.value = 'Your basket is empty. Add dishes from the menu before checking out.'
    return
  }

  isPlacing.value = true
  paymentError.value = null

  const raw_items = summaryItems.value.map((si) => ({
    menuItemId: si.item.id,
    quantity: si.quantity,
  }))

  try {
    // 1. Create order in backend.
    const orderRes = await restroHandler.orders.create({
      order_type: 'Delivery',
      customer_name: customerName.value || 'Gourmet Guest',
      customer_phone: customerPhone.value || '+91 98765 43210',
      delivery_address: address.value,
      delivery_instructions: instructions.value,
      raw_items,
    })

    const newOrderId = orderRes?.id || 'SHP-9482'
    placedOrderId.value = String(newOrderId).replace('#', '')

    // 2. Cash on Delivery: order is confirmed as soon as it is created.
    if (paymentMethod.value !== 'Razorpay') {
      finalizeOrder()
      return
    }

    // 3. Razorpay: create the gateway order, open checkout, then verify.
    const rzpOrder = await restroHandler.orders.createRazorpayOrder({
      amount: grandTotal.value,
      order_id: newOrderId,
      customer_name: customerName.value,
      customer_phone: customerPhone.value,
    })

    const paymentRes = await openRazorpayCheckout({
      key: rzpOrder.key_id,
      amount: rzpOrder.amount,
      currency: rzpOrder.currency || 'INR',
      name: 'SHP Restro',
      description: `Delivery Order ${newOrderId}`,
      order_id: rzpOrder.razorpay_order_id,
      prefill: {
        name: customerName.value,
        contact: customerPhone.value,
      },
      theme: {
        color: '#f47b20',
      },
    })

    // 4. Verify the payment with the backend BEFORE confirming anything.
    await restroHandler.orders.verifyRazorpayPayment({
      order_id: newOrderId,
      razorpay_order_id: paymentRes.razorpay_order_id,
      razorpay_payment_id: paymentRes.razorpay_payment_id,
      razorpay_signature: paymentRes.razorpay_signature,
    })

    // Success continuation only: payment is verified, so confirm & clear the cart.
    paymentId.value = paymentRes.razorpay_payment_id
    finalizeOrder()
  } catch (err: unknown) {
    // Any failure (create, Razorpay order, checkout, dismissal, or verification):
    // surface the error and keep the cart intact. Never confirm the order here.
    const apiMessage = getApiErrorMessage(err)
    paymentError.value =
      apiMessage === 'An unexpected error occurred.' && err instanceof Error
        ? err.message
        : apiMessage
  } finally {
    isPlacing.value = false
  }
}
</script>

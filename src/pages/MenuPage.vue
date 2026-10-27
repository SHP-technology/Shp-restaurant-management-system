<template>
  <div class="min-h-screen bg-[#faf8f5] text-[#1a1f1c] flex flex-col justify-between selection:bg-orange-500 selection:text-white">
    <!-- Sticky App Header -->
    <AppHeader />

    <!-- Hero / Headline Bar -->
    <section class="bg-linear-to-b from-orange-50/70 via-[#faf8f5] to-[#faf8f5] pt-6 sm:pt-8 pb-4 sm:pb-6 border-b border-orange-100/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-100/90 text-[#ea580c] text-xs font-black tracking-wide uppercase mb-2 shadow-2xs">
              <Sparkles :size="13" class="text-orange-500 animate-spin-slow" />
              <span>Gourmet Signature Menu</span>
            </div>
            <h1 class="font-heading text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-slate-900 tracking-tight leading-tight">
              Handcrafted with Culinary Passion.
            </h1>
            <p class="text-xs sm:text-sm md:text-base text-slate-600 mt-1 sm:mt-1.5 max-w-2xl font-normal">
              Fresh farm-to-table ingredients, authentic slow-cooking heritage, and modern culinary precision.
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-2 sm:gap-3">
            <span class="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-700 text-xs font-bold px-3 py-1.5 rounded-full border border-emerald-200/90 shadow-2xs">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Live Kitchen Online (11:00 AM – 11:30 PM)
            </span>
            <span class="inline-flex items-center gap-1 bg-amber-50 text-amber-800 text-xs font-bold px-3 py-1.5 rounded-full border border-amber-200/80 shadow-2xs">
              <Clock :size="13" class="text-amber-600" />
              Avg. 25-30m Delivery
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Sticky Sub-Bar: Categories, Search, Filters -->
    <div class="sticky top-[68px] sm:top-[72px] z-30 bg-white/95 backdrop-blur-xl border-b border-slate-200/80 shadow-xs px-3 sm:px-6 py-3 transition-all">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
        <!-- Category Navigation: Swipeable Chips Bar with Count Badges -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 scrollbar-none snap-x touch-pan-x">
          <button
            v-for="cat in categoryList"
            :key="cat.name"
            @click="selectedCategory = cat.name"
            :class="[
              'rounded-xl px-3 sm:px-4 py-2 text-xs font-bold transition-all duration-200 shrink-0 snap-start cursor-pointer flex items-center gap-1.5 select-none border',
              selectedCategory === cat.name
                ? 'bg-slate-900 border-slate-900 text-white shadow-md shadow-slate-900/15 scale-[1.02]'
                : 'bg-slate-50 border-slate-200/80 text-slate-700 hover:bg-slate-100 hover:border-slate-300'
            ]"
          >
            <span>{{ cat.icon }}</span>
            <span>{{ cat.name }}</span>
            <span
              :class="[
                'text-[10px] px-1.5 py-0.5 rounded-full font-black ml-0.5 transition-colors',
                selectedCategory === cat.name
                  ? 'bg-orange-500 text-white'
                  : 'bg-slate-200 text-slate-600'
              ]"
            >
              {{ cat.count }}
            </span>
          </button>
        </div>

        <!-- Controls: Search & Pure Veg Toggle -->
        <div class="flex items-center gap-2 sm:gap-3 w-full md:w-auto">
          <!-- Search Input -->
          <div class="relative flex-1 md:w-64 lg:w-72">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-3.5 h-3.5 sm:w-4 sm:h-4" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search dishes, ingredients..."
              class="w-full rounded-xl border border-slate-200 bg-slate-50/80 pl-9 pr-7 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:border-orange-500 focus:bg-white focus:outline-none focus:ring-3 focus:ring-orange-500/10 transition-all"
            />
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs p-0.5"
              aria-label="Clear search"
            >
              ✕
            </button>
          </div>

          <!-- Pure Veg Toggle -->
          <button
            @click="vegOnlyFilter = !vegOnlyFilter"
            :class="[
              'flex items-center gap-1.5 sm:gap-2 rounded-xl border px-3 sm:px-3.5 py-2 text-xs font-bold transition-all duration-200 shrink-0 cursor-pointer select-none',
              vegOnlyFilter
                ? 'border-emerald-500 bg-emerald-50 text-emerald-800 shadow-xs ring-2 ring-emerald-500/20'
                : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
            ]"
          >
            <div class="w-3.5 h-3.5 border-2 border-emerald-600 flex items-center justify-center p-0.5 rounded-xs">
              <div class="w-1.5 h-1.5 rounded-full" :class="vegOnlyFilter ? 'bg-emerald-600' : 'bg-transparent'"></div>
            </div>
            <span class="whitespace-nowrap">Pure Veg</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10 flex-1 w-full">
      <!-- Loading Skeleton State -->
      <div v-if="isLoading" class="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        <div
          v-for="n in 8"
          :key="n"
          class="rounded-3xl border border-slate-200/80 bg-white p-4 animate-pulse space-y-4"
        >
          <div class="h-44 sm:h-48 bg-slate-200 rounded-2xl w-full"></div>
          <div class="space-y-2">
            <div class="h-4 bg-slate-200 rounded w-3/4"></div>
            <div class="h-3 bg-slate-100 rounded w-full"></div>
            <div class="h-3 bg-slate-100 rounded w-1/2"></div>
          </div>
          <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
            <div class="h-6 bg-slate-200 rounded w-16"></div>
            <div class="h-8 bg-slate-200 rounded-xl w-24"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        class="text-center py-16 sm:py-20 bg-white rounded-3xl border border-rose-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center text-3xl mx-auto mb-4 border border-rose-100">
          ⚠️
        </div>
        <h3 class="text-base sm:text-lg font-black text-slate-900 font-heading">
          Unable to Load the Menu
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1.5 max-w-sm mx-auto leading-relaxed">
          {{ error }}
        </p>
        <button
          @click="loadMenu"
          class="mt-5 text-xs font-bold text-white bg-slate-900 px-5 py-2.5 rounded-xl hover:bg-orange-600 transition-colors shadow-sm cursor-pointer active:scale-95"
        >
          Retry
        </button>
      </div>

      <!-- Backend Empty State (no dishes at all) -->
      <div
        v-else-if="items.length === 0"
        class="text-center py-16 sm:py-20 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-orange-50 text-[#ea580c] flex items-center justify-center text-3xl mx-auto mb-4 border border-orange-100">
          🍽️
        </div>
        <h3 class="text-base sm:text-lg font-black text-slate-900 font-heading">
          Menu Coming Soon
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1.5 max-w-sm mx-auto leading-relaxed">
          Our chefs are updating the menu. Please check back shortly for our latest culinary creations.
        </p>
      </div>

      <!-- Filtered Empty State -->
      <div
        v-else-if="filteredItems.length === 0"
        class="text-center py-16 sm:py-20 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 max-w-lg mx-auto shadow-xs"
      >
        <div class="w-16 h-16 rounded-2xl bg-orange-50 text-[#ea580c] flex items-center justify-center text-3xl mx-auto mb-4 border border-orange-100">
          🍽️
        </div>
        <h3 class="text-base sm:text-lg font-black text-slate-900 font-heading">
          No Culinary Creations Found
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1.5 max-w-sm mx-auto leading-relaxed">
          We couldn't find any dishes matching "{{ searchQuery || selectedCategory }}". Try selecting a different category or clearing active filters.
        </p>
        <button
          @click="resetFilters"
          class="mt-5 text-xs font-bold text-white bg-slate-900 px-5 py-2.5 rounded-xl hover:bg-orange-600 transition-colors shadow-sm cursor-pointer active:scale-95"
        >
          Reset Filters & View Full Menu
        </button>
      </div>

      <!-- Dish Cards Responsive Grid: 1 col on mobile, 2 on tablet, 3-4 on desktop -->
      <div
        v-else
        class="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-4"
      >
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="group flex flex-col justify-between overflow-hidden rounded-3xl border border-slate-200/80 bg-white p-4 sm:p-5 shadow-xs transition-all duration-300 hover:shadow-xl hover:border-orange-200 hover:-translate-y-1"
        >
          <div>
            <!-- Dish Image + Badges -->
            <div class="relative mb-3.5 sm:mb-4 h-44 sm:h-48 overflow-hidden rounded-2xl bg-slate-100">
              <img
                :src="item.image"
                :alt="item.name"
                class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                loading="lazy"
                @error="handleImageError($event)"
              />
              <div class="absolute inset-0 bg-linear-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

              <!-- Veg / Non-Veg FSSAI Badge -->
              <div class="absolute top-2.5 left-2.5 bg-white/95 backdrop-blur-md p-1 rounded-lg shadow-xs flex items-center gap-1.5 px-2 border border-slate-100">
                <div
                  class="w-3 h-3 sm:w-3.5 sm:h-3.5 border-2 flex items-center justify-center rounded-xs"
                  :class="item.isVeg ? 'border-emerald-600' : 'border-rose-600'"
                >
                  <div class="w-1.5 h-1.5 rounded-full" :class="item.isVeg ? 'bg-emerald-600' : 'bg-rose-600'"></div>
                </div>
                <span class="text-[9px] sm:text-[10px] font-black uppercase tracking-wider" :class="item.isVeg ? 'text-emerald-700' : 'text-rose-700'">
                  {{ item.isVeg ? 'Veg' : 'Non-Veg' }}
                </span>
              </div>

              <!-- Rating Badge (only when backend provides a rating) -->
              <div
                v-if="item.rating"
                class="absolute top-2.5 right-2.5 bg-white/95 backdrop-blur-md px-2 py-1 rounded-lg shadow-xs flex items-center gap-1 text-[10px] sm:text-[11px] font-black text-amber-700 border border-slate-100"
              >
                <Star :size="11" class="fill-amber-400 text-amber-400" />
                <span>{{ Number(item.rating).toFixed(1) }}</span>
              </div>

              <!-- Chef's Signature Badge -->
              <div
                v-if="item.isSpecial"
                class="absolute bottom-2.5 left-2.5 bg-linear-to-r from-amber-500 to-orange-500 text-white text-[9px] sm:text-[10px] font-black px-2.5 py-0.5 rounded-full shadow-md flex items-center gap-1"
              >
                <span>⭐ Chef's Signature</span>
              </div>
            </div>

            <!-- Dish Title & Description -->
            <div class="space-y-1">
              <div class="flex items-start justify-between gap-2">
                <h3 class="font-heading font-bold text-base sm:text-lg text-slate-900 group-hover:text-orange-600 transition-colors line-clamp-1">
                  {{ item.name }}
                </h3>
              </div>
              <p v-if="item.description" class="text-xs text-slate-500 leading-relaxed line-clamp-2">
                {{ item.description }}
              </p>
            </div>
          </div>

          <!-- Price & Stepper CTA -->
          <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
            <div>
              <div class="font-heading font-black text-lg sm:text-xl text-slate-900">
                ₹{{ Number(item.price).toFixed(0) }}
              </div>
              <div v-if="item.prepTime || item.prep_time" class="text-[10px] text-slate-400 flex items-center gap-1">
                <Clock :size="10" /> {{ item.prepTime || item.prep_time }}
              </div>
            </div>

            <!-- Quantity Stepper if in Cart -->
            <div
              v-if="cartStore.getItemQuantity(item.id) > 0"
              class="flex items-center gap-1.5 bg-orange-50 border border-orange-200 rounded-xl p-0.5 sm:p-1 shadow-xs"
            >
              <button
                @click="cartStore.decrementItem(item.id)"
                class="w-7 h-7 rounded-lg bg-white text-orange-600 font-black text-sm flex items-center justify-center hover:bg-orange-600 hover:text-white transition-all cursor-pointer shadow-2xs active:scale-90"
                aria-label="Decrease quantity"
              >
                -
              </button>
              <span class="text-xs font-black text-orange-800 min-w-5 text-center">
                {{ cartStore.getItemQuantity(item.id) }}
              </span>
              <button
                @click="cartStore.addItem(item)"
                class="w-7 h-7 rounded-lg bg-orange-500 text-white font-black text-sm flex items-center justify-center hover:bg-orange-600 transition-all cursor-pointer shadow-2xs active:scale-90"
                aria-label="Increase quantity"
              >
                +
              </button>
            </div>

            <!-- Add Button if not in Cart -->
            <button
              v-else
              @click="cartStore.addItem(item)"
              class="rounded-xl bg-slate-900 px-3.5 py-2 sm:px-4 sm:py-2.5 text-xs font-bold text-white shadow-xs hover:bg-orange-600 transition-all flex items-center gap-1.5 cursor-pointer active:scale-95"
            >
              <Plus :size="14" />
              <span>Add</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Floating Sticky Cart Drawer & Checkout Bar -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-8 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-8 scale-95"
    >
      <div
        v-if="cartStore.totalCount > 0"
        class="fixed bottom-4 left-3 right-3 sm:bottom-6 sm:left-auto sm:right-6 sm:w-96 z-40"
      >
        <div class="bg-white/95 text-slate-900 p-3.5 sm:p-4 rounded-2xl sm:rounded-3xl shadow-2xl border border-slate-200 flex items-center justify-between gap-3 backdrop-blur-xl ring-1 ring-slate-900/5">
          <button
            @click="showCartDrawer = !showCartDrawer"
            class="flex items-center gap-3 text-left cursor-pointer group"
          >
            <div class="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center font-bold border border-orange-200 group-hover:scale-105 transition-transform">
              <ShoppingBag :size="18" />
            </div>
            <div>
              <div class="text-[10px] sm:text-[11px] font-bold text-orange-600 uppercase tracking-wider flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-orange-500 animate-pulse"></span>
                {{ cartStore.totalCount }} {{ cartStore.totalCount === 1 ? 'Dish' : 'Dishes' }} Selected
              </div>
              <div class="font-heading text-lg sm:text-xl font-black text-slate-900">
                ₹{{ cartStore.grandTotal }}
                <span class="text-[10px] font-normal text-slate-500">(incl. GST)</span>
              </div>
            </div>
          </button>

          <div class="flex items-center gap-2">
            <button
              @click="showCartDrawer = !showCartDrawer"
              class="hidden sm:inline-flex items-center justify-center px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold cursor-pointer transition-colors"
              title="Toggle Cart Drawer"
            >
              {{ showCartDrawer ? 'Hide' : 'Review' }}
            </button>
            <RouterLink
              to="/delivery"
              class="orange-button px-4 sm:px-5 py-2.5 sm:py-3 rounded-xl sm:rounded-2xl font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-orange-500/30 active:scale-95 whitespace-nowrap"
            >
              <span>Order Now</span>
              <ArrowRight :size="14" />
            </RouterLink>
          </div>
        </div>
      </div>
    </transition>

    <!-- Slide-Over / Bottom Drawer for Itemized Cart Preview -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-full sm:translate-y-0 sm:translate-x-full"
      enter-to-class="opacity-100 translate-y-0 sm:translate-x-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0 sm:translate-x-0"
      leave-to-class="opacity-0 translate-y-full sm:translate-y-0 sm:translate-x-full"
    >
      <div
        v-if="showCartDrawer && cartStore.totalCount > 0"
        class="fixed inset-y-0 right-0 z-50 w-full sm:w-96 bg-white shadow-2xl border-l border-slate-200 flex flex-col justify-between"
      >
        <!-- Drawer Header -->
        <div class="p-4 sm:p-5 border-b border-slate-100 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold">
              <ShoppingBag :size="16" />
            </div>
            <div>
              <h3 class="font-heading font-black text-base text-slate-900">Your Basket</h3>
              <p class="text-[10px] text-slate-400">{{ cartStore.totalCount }} items added</p>
            </div>
          </div>
          <button
            @click="showCartDrawer = false"
            class="w-8 h-8 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-sm font-bold cursor-pointer transition-colors"
          >
            ✕
          </button>
        </div>

        <!-- Drawer Item List -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 divide-y divide-slate-100">
          <div
            v-for="ci in cartStore.items"
            :key="ci.item.id"
            class="py-3 flex items-center justify-between gap-3"
          >
            <div class="flex items-center gap-3">
              <img
                :src="ci.item.image"
                :alt="ci.item.name"
                class="w-12 h-12 rounded-xl object-cover bg-slate-100 shrink-0"
                @error="handleImageError($event)"
              />
              <div class="min-w-0">
                <h4 class="text-xs font-bold text-slate-900 truncate">{{ ci.item.name }}</h4>
                <div class="text-[11px] font-black text-orange-600">
                  ₹{{ ci.item.price }} <span class="text-slate-400 text-[10px] font-normal">× {{ ci.quantity }}</span>
                </div>
              </div>
            </div>

            <!-- Mini Stepper -->
            <div class="flex items-center gap-1.5 bg-slate-100 rounded-lg p-0.5">
              <button
                @click="cartStore.decrementItem(ci.item.id)"
                class="w-6 h-6 rounded-md bg-white text-slate-700 font-black text-xs flex items-center justify-center hover:bg-orange-600 hover:text-white transition-colors cursor-pointer shadow-2xs"
              >
                -
              </button>
              <span class="text-xs font-bold text-slate-900 min-w-4 text-center">{{ ci.quantity }}</span>
              <button
                @click="cartStore.addItem(ci.item)"
                class="w-6 h-6 rounded-md bg-white text-slate-700 font-black text-xs flex items-center justify-center hover:bg-orange-600 hover:text-white transition-colors cursor-pointer shadow-2xs"
              >
                +
              </button>
            </div>
          </div>
        </div>

        <!-- Drawer Footer -->
        <div class="p-4 sm:p-5 border-t border-slate-100 bg-slate-50 space-y-3">
          <div class="space-y-1.5 text-xs text-slate-600">
            <div class="flex justify-between">
              <span>Subtotal</span>
              <span class="font-bold text-slate-900">₹{{ cartStore.subtotal }}</span>
            </div>
            <div class="flex justify-between">
              <span>GST (5%)</span>
              <span class="font-bold text-slate-900">₹{{ cartStore.gstAmount }}</span>
            </div>
            <div class="flex justify-between border-t border-slate-200 pt-1.5 text-sm font-black text-slate-900 font-heading">
              <span>Grand Total</span>
              <span class="text-orange-600 font-black">₹{{ cartStore.grandTotal }}</span>
            </div>
          </div>

          <div class="flex items-center gap-2 pt-1">
            <button
              @click="cartStore.clearCart()"
              class="px-3 py-3 rounded-xl bg-slate-200 hover:bg-rose-100 hover:text-rose-700 text-slate-700 font-bold text-xs transition-colors cursor-pointer"
            >
              Clear
            </button>
            <RouterLink
              to="/delivery"
              class="flex-1 orange-button py-3 rounded-xl font-bold text-xs text-center flex items-center justify-center gap-1.5 shadow-md shadow-orange-500/20"
            >
              <span>Proceed to Checkout</span>
              <ArrowRight :size="14" />
            </RouterLink>
          </div>
        </div>
      </div>
    </transition>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Search, Star, Plus, ArrowRight, Clock, Sparkles, ShoppingBag } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler, type MenuItemData } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()
const isLoading = ref(true)
const error = ref('')
const showCartDrawer = ref(false)

const items = ref<MenuItemData[]>([])
const selectedCategory = ref('All')
const searchQuery = ref('')
const vegOnlyFilter = ref(false)

const categoryIcons: Record<string, string> = {
  All: '🍽️',
  Starters: '🥟',
  Mains: '🍛',
  Pizzas: '🍕',
  Burgers: '🍔',
  Desserts: '🍰',
  Beverages: '🥤',
}

async function loadMenu() {
  isLoading.value = true
  error.value = ''
  try {
    const dishes = await restroHandler.menu.list()
    items.value = (Array.isArray(dishes) ? dishes : []).map((d): MenuItemData => ({
      id: Number(d.id),
      name: d.name,
      price: Number(d.price),
      category: d.category || 'Mains',
      description: d.description || '',
      rating: d.rating,
      prepTime: d.prepTime ?? d.prep_time,
      isVeg: d.isVeg ?? d.is_veg ?? false,
      isSpecial: d.isSpecial ?? d.is_special ?? false,
      image: d.image,
    }))
  } catch (err) {
    error.value = getApiErrorMessage(err)
    items.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(loadMenu)

const categoryList = computed(() => {
  const dynamicCategories = Array.from(new Set(items.value.map((i) => i.category || 'Mains'))).filter(Boolean)
  const allCategoryNames = ['All', ...dynamicCategories]

  return allCategoryNames.map((catName) => {
    let count = 0
    if (catName === 'All') {
      count = items.value.length
    } else {
      count = items.value.filter((i) => (i.category || 'Mains') === catName).length
    }
    return {
      name: catName,
      icon: categoryIcons[catName] || '✨',
      count,
    }
  })
})

const filteredItems = computed(() => {
  return items.value.filter((item) => {
    const itemCat = item.category || 'Mains'
    const matchesCategory = selectedCategory.value === 'All' || itemCat.toLowerCase() === selectedCategory.value.toLowerCase()
    const query = searchQuery.value.trim().toLowerCase()
    const matchesSearch =
      !query ||
      item.name.toLowerCase().includes(query) ||
      (item.description && item.description.toLowerCase().includes(query)) ||
      itemCat.toLowerCase().includes(query)
    const matchesVeg = !vegOnlyFilter.value || Boolean(item.isVeg)
    return matchesCategory && matchesSearch && matchesVeg
  })
})

function resetFilters() {
  selectedCategory.value = 'All'
  searchQuery.value = ''
  vegOnlyFilter.value = false
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  if (img) {
    img.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
  }
}
</script>

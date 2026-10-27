<template>
  <div class="min-h-screen bg-[#fffdf9] text-[#1d211e] flex flex-col justify-between">
    <!-- Sticky App Header -->
    <AppHeader />

    <main class="grow">
      <!-- Hero Section -->
      <section class="relative overflow-hidden bg-linear-to-b from-orange-50/50 via-white to-[#fffdf9] py-10 sm:py-16 lg:py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-center">
            <!-- Left Hero Content -->
            <div class="lg:col-span-7 space-y-6 text-left">
              <div
                v-if="restaurant?.tagline"
                class="inline-flex items-center gap-2 rounded-full bg-orange-100/90 border border-orange-200/80 px-4 py-1.5 text-xs font-bold text-[#f47b20] shadow-xs"
              >
                <Sparkles :size="14" class="animate-pulse" /> {{ restaurant.tagline }}
              </div>

              <h1 class="font-heading text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-900 leading-tight sm:leading-[1.1]">
                Culinary Perfection <br />
                <span class="text-[#f47b20]">Delivered to Your Table.</span>
              </h1>

              <p v-if="restaurant?.description" class="text-sm sm:text-base lg:text-lg text-gray-600 max-w-xl leading-relaxed">
                {{ restaurant.description }}
              </p>

              <!-- CTA Actions -->
              <div class="flex flex-wrap items-center gap-3.5 pt-1">
                <RouterLink
                  to="/menu"
                  class="orange-button px-6 sm:px-7 py-3.5 rounded-xl font-bold text-sm flex items-center gap-2.5 shadow-lg shadow-orange-500/25 min-h-[48px]"
                >
                  <ShoppingBag :size="18" />
                  <span>Explore Dine-In Menu</span>
                </RouterLink>

                <RouterLink
                  to="/booking"
                  class="bg-white hover:bg-gray-50 text-gray-800 border border-gray-200 px-6 sm:px-7 py-3.5 rounded-xl font-bold text-sm flex items-center gap-2 transition-all shadow-xs min-h-[48px]"
                >
                  <CalendarDays :size="18" class="text-[#f47b20]" />
                  <span>Reserve a Table</span>
                </RouterLink>
              </div>
            </div>

            <!-- Right Hero Visual Card -->
            <div v-if="restaurant?.hero_image" class="lg:col-span-5 relative mt-4 lg:mt-0">
              <div class="relative overflow-hidden rounded-3xl shadow-2xl border-4 border-white bg-gray-100 group">
                <img
                  :src="restaurant.hero_image"
                  :alt="restaurant.name || 'Restaurant Food & Ambiance'"
                  class="h-[320px] sm:h-[420px] lg:h-[460px] w-full object-cover transition-transform duration-700 group-hover:scale-105"
                  loading="eager"
                />

                <!-- Floating Live Orders Ticker -->
                <div class="absolute top-4 right-4 bg-gray-900/85 backdrop-blur-md text-white text-[11px] font-bold px-3 py-1.5 rounded-full shadow-lg flex items-center gap-1.5 border border-white/10">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span>Live Kitchen Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Live Services Grid -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <div class="text-center max-w-2xl mx-auto mb-10">
          <span class="text-xs font-bold uppercase tracking-widest text-[#f47b20] bg-orange-50 px-3 py-1 rounded-full border border-orange-100">
            Our Experiences
          </span>
          <h2 class="font-heading text-2xl sm:text-4xl font-extrabold text-gray-900 mt-2.5">
            Everything You Need Under One Roof
          </h2>
          <p class="text-xs sm:text-sm text-gray-500 mt-2">
            Seamlessly switch between fine dining table reservations, express delivery, and banquet celebrations.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 sm:gap-6">
          <RouterLink
            v-for="srv in services"
            :key="srv.title"
            :to="srv.link"
            class="group p-6 rounded-2xl bg-white border border-gray-200/80 shadow-xs transition-all duration-200 hover:shadow-xl hover:border-orange-300 hover:-translate-y-1 flex flex-col justify-between"
          >
            <div>
              <div class="h-12 w-12 rounded-2xl bg-orange-50 flex items-center justify-center text-[#f47b20] mb-4 group-hover:scale-110 group-hover:bg-[#f47b20] group-hover:text-white transition-all shadow-2xs">
                <component :is="srv.icon" :size="22" />
              </div>
              <h3 class="font-heading font-bold text-lg text-gray-900 group-hover:text-[#f47b20] transition-colors">
                {{ srv.title }}
              </h3>
              <p class="text-xs sm:text-sm text-gray-500 mt-2 leading-relaxed">
                {{ srv.description }}
              </p>
            </div>
            <div class="mt-6 flex items-center gap-1.5 text-xs font-bold text-[#f47b20] group-hover:translate-x-1.5 transition-transform">
              <span>Explore Now</span>
              <ArrowRight :size="14" />
            </div>
          </RouterLink>
        </div>
      </section>

      <!-- Popular Signature Menu Dishes Preview -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 bg-white border-y border-gray-100">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
          <div>
            <span class="text-xs font-bold uppercase tracking-widest text-[#f47b20] bg-orange-50 px-3 py-1 rounded-full border border-orange-100">
              Chef's Recommendations
            </span>
            <h2 class="font-heading text-2xl sm:text-4xl font-extrabold text-gray-900 mt-2.5">
              Signature Delicacies
            </h2>
            <p class="text-xs sm:text-sm text-gray-500 mt-1">
              Hand-picked favorites prepared fresh with authentic seasonings.
            </p>
          </div>
          <RouterLink
            to="/menu"
            class="inline-flex items-center gap-1.5 text-xs sm:text-sm font-bold text-[#f47b20] hover:text-[#d9630f] transition-colors py-1 self-start sm:self-auto"
          >
            <span>View Full Menu</span>
            <ArrowRight :size="16" />
          </RouterLink>
        </div>

        <!-- Loading Skeleton -->
        <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5 sm:gap-5">
          <div
            v-for="n in 5"
            :key="n"
            class="p-3.5 sm:p-4 rounded-2xl bg-white border border-gray-200/80 shadow-xs animate-pulse"
          >
            <div class="mb-3 h-32 sm:h-36 w-full rounded-xl bg-gray-200"></div>
            <div class="h-3.5 bg-gray-200 rounded w-3/4"></div>
            <div class="mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
              <div class="h-4 bg-gray-200 rounded w-12"></div>
              <div class="h-6 bg-gray-200 rounded-lg w-12"></div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div
          v-else-if="error"
          class="text-center py-12 bg-orange-50/50 rounded-2xl border border-orange-100 max-w-lg mx-auto"
        >
          <p class="text-sm font-bold text-gray-900">Unable to load dishes</p>
          <p class="text-xs text-gray-500 mt-1.5 max-w-sm mx-auto">{{ error }}</p>
          <button
            @click="loadData"
            class="mt-4 text-xs font-bold text-white bg-[#f47b20] px-5 py-2.5 rounded-xl hover:bg-[#d9630f] transition-colors cursor-pointer"
          >
            Retry
          </button>
        </div>

        <!-- Empty State -->
        <div
          v-else-if="menuPreview.length === 0"
          class="text-center py-12 bg-white rounded-2xl border border-gray-200/80 max-w-lg mx-auto"
        >
          <p class="text-sm font-bold text-gray-900">No dishes available yet</p>
          <p class="text-xs text-gray-500 mt-1.5">Our chefs are updating the menu. Please check back soon.</p>
        </div>

        <!-- Dishes Grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5 sm:gap-5">
          <div
            v-for="dish in menuPreview"
            :key="dish.id"
            class="group p-3.5 sm:p-4 rounded-2xl bg-white border border-gray-200/80 shadow-xs hover:shadow-lg hover:border-orange-300 transition-all flex flex-col justify-between"
          >
            <div>
              <div class="relative mb-3 h-32 sm:h-36 w-full overflow-hidden rounded-xl bg-gray-100">
                <img
                  :src="dish.image"
                  :alt="dish.name"
                  class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  loading="lazy"
                />
              </div>
              <h4 class="font-bold text-xs sm:text-sm text-gray-900 line-clamp-1 group-hover:text-[#f47b20] transition-colors" :title="dish.name">
                {{ dish.name }}
              </h4>
            </div>
            <div class="mt-3 sm:mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
              <span class="font-heading font-extrabold text-sm sm:text-base text-[#f47b20]">₹{{ dish.price }}</span>
              <RouterLink
                to="/menu"
                class="rounded-lg bg-gray-900 px-2.5 sm:px-3 py-1.5 text-xs font-bold text-white hover:bg-[#f47b20] transition-colors"
              >
                + Add
              </RouterLink>
            </div>
          </div>
        </div>
      </section>

      <!-- Why Choose Us / Trust Pillars -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="p-5 rounded-2xl bg-orange-50/50 border border-orange-100/80 flex items-start gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-[#f47b20] text-white flex items-center justify-center font-bold shrink-0 shadow-xs">
              👨‍🍳
            </div>
            <div>
              <h4 class="font-bold text-sm text-gray-900">Master Chefs</h4>
              <p class="text-xs text-gray-500 mt-1 leading-relaxed">Curated recipes with decades of royal culinary heritage.</p>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-orange-50/50 border border-orange-100/80 flex items-start gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-[#f47b20] text-white flex items-center justify-center font-bold shrink-0 shadow-xs">
              🌿
            </div>
            <div>
              <h4 class="font-bold text-sm text-gray-900">Organic & Fresh</h4>
              <p class="text-xs text-gray-500 mt-1 leading-relaxed">Locally sourced farm produce with zero artificial additives.</p>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-orange-50/50 border border-orange-100/80 flex items-start gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-[#f47b20] text-white flex items-center justify-center font-bold shrink-0 shadow-xs">
              ⚡
            </div>
            <div>
              <h4 class="font-bold text-sm text-gray-900">Instant Reservations</h4>
              <p class="text-xs text-gray-500 mt-1 leading-relaxed">Guaranteed seating without waiting in line during rush hours.</p>
            </div>
          </div>

          <div class="p-5 rounded-2xl bg-orange-50/50 border border-orange-100/80 flex items-start gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-[#f47b20] text-white flex items-center justify-center font-bold shrink-0 shadow-xs">
              🛡️
            </div>
            <div>
              <h4 class="font-bold text-sm text-gray-900">5-Star Hygiene</h4>
              <p class="text-xs text-gray-500 mt-1 leading-relaxed">FSSAI certified sanitized kitchen and contactless delivery.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Instant Table Reservation & Banquet Banner -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-14">
        <div class="relative overflow-hidden rounded-3xl bg-linear-to-br from-orange-500 via-orange-600 to-amber-600 p-6 sm:p-12 lg:p-14 text-white shadow-xl shadow-orange-500/20 border border-orange-400/30">
          <!-- Background Decorative Glow -->
          <div class="absolute -right-20 -top-20 w-80 h-80 rounded-full bg-white/10 blur-3xl pointer-events-none"></div>
          <div class="absolute -left-20 -bottom-20 w-80 h-80 rounded-full bg-amber-300/20 blur-3xl pointer-events-none"></div>

          <div class="relative z-10 max-w-2xl space-y-4">
            <span class="inline-flex items-center gap-2 rounded-full bg-white/20 px-3.5 py-1 text-xs font-bold text-white backdrop-blur-xs border border-white/20">
              <CalendarDays :size="14" /> Seamless Dining & Celebrations
            </span>
            <h2 class="font-heading text-2xl sm:text-4xl lg:text-5xl font-extrabold leading-tight text-white">
              Planning a Special Dinner or Family Gathering?
            </h2>
            <p class="text-xs sm:text-sm lg:text-base text-orange-100 leading-relaxed font-medium">
              Skip the waiting queue. Book your preferred seating zone—Main Dining, Open Rooftop, or VIP Private Booth in under 60 seconds.
            </p>
            <div class="pt-3 flex flex-wrap gap-3.5">
              <RouterLink
                to="/booking"
                class="bg-white text-orange-600 hover:bg-orange-50 px-6 sm:px-7 py-3.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg min-h-[44px] transition-all"
              >
                <span>Reserve Table Now</span>
                <ArrowRight :size="16" />
              </RouterLink>
              <RouterLink
                to="/party-booking"
                class="bg-black/15 hover:bg-black/25 text-white border border-white/30 px-5 sm:px-6 py-3.5 rounded-xl font-bold text-xs sm:text-sm backdrop-blur-xs transition-colors min-h-[44px] flex items-center justify-center"
              >
                Explore Banquet Hall Packages
              </RouterLink>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Unified Footer -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import {
  CalendarDays,
  ShoppingBag,
  Truck,
  UsersRound,
  ArrowRight,
  Sparkles,
  MapPin,
} from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import { restroHandler, type MenuItemData, type RestaurantData } from '../services/api'
import { getApiErrorMessage } from '../services/api/client'

const restaurant = ref<RestaurantData | null>(null)
const menuPreview = ref<MenuItemData[]>([])
const isLoading = ref(true)
const error = ref('')

const services = [
  { icon: CalendarDays, title: 'Table Reservation', description: 'Reserve your favorite table instantly with customized seating.', link: '/booking' },
  { icon: Truck, title: 'Doorstep Delivery', description: 'Fresh, piping hot gourmet meals delivered in under 30 minutes.', link: '/delivery' },
  { icon: UsersRound, title: 'Party & Celebrations', description: 'Full-service catering, decorations, and dedicated event halls.', link: '/party-booking' },
  { icon: MapPin, title: 'Live Order Tracking', description: 'Track your food in real-time from the kitchen to your table or home.', link: '/delivery' },
]

async function loadData() {
  isLoading.value = true
  error.value = ''
  try {
    const [restData, dishes] = await Promise.all([
      restroHandler.restaurants.getCurrent(),
      restroHandler.menu.list(),
    ])
    restaurant.value = restData ?? null
    menuPreview.value = Array.isArray(dishes) ? dishes.slice(0, 5) : []
  } catch (err) {
    error.value = getApiErrorMessage(err)
    restaurant.value = null
    menuPreview.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(loadData)
</script>

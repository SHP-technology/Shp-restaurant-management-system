<template>
  <div class="min-h-screen bg-[#f7f5f0] text-[#1a1917] font-sans">
    <!-- Main Navbar -->
    <header class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <RouterLink to="/" class="flex items-center gap-2.5">
          <img src="/logo.png" alt="SHP Restaurant Logo" class="h-9 w-9 rounded-lg object-cover shadow-sm" />
          <span class="font-heading text-2xl font-black tracking-tight text-gray-900">
            SHP<span class="text-[#f47b20]">.</span>
          </span>
        </RouterLink>

        <!-- Desktop Links -->
        <nav class="hidden md:flex items-center gap-6 text-xs font-semibold text-gray-700">
          <RouterLink to="/" class="text-[#f47b20] transition">Home</RouterLink>
          <RouterLink to="/menu" class="hover:text-[#f47b20] transition">Menu</RouterLink>
          <RouterLink to="/booking" class="hover:text-[#f47b20] transition">Table Booking</RouterLink>
          <RouterLink to="/delivery" class="hover:text-[#f47b20] transition">Delivery</RouterLink>
          <RouterLink to="/party-booking" class="hover:text-[#f47b20] transition">Party Hall</RouterLink>
          <RouterLink to="/offers" class="hover:text-[#f47b20] transition">Offers</RouterLink>
          <RouterLink to="/contact" class="hover:text-[#f47b20] transition">Contact</RouterLink>
        </nav>

        <div class="flex items-center gap-3">
          <RouterLink
            to="/login"
            class="hidden sm:inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-3.5 py-1.5 text-xs font-bold text-gray-800 shadow-sm transition hover:bg-gray-50"
          >
            Staff Login
          </RouterLink>
          <RouterLink
            to="/menu"
            class="inline-flex items-center justify-center rounded-lg bg-[#f47b20] px-4 py-2 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f]"
          >
            Order Food
          </RouterLink>
          <button
            class="md:hidden text-gray-700 p-1"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <component :is="mobileMenuOpen ? X : Menu" :size="20" />
          </button>
        </div>
      </div>

      <!-- Mobile Dropdown -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200 bg-white p-4 space-y-3 text-xs font-bold">
        <RouterLink to="/" class="block py-1 text-[#f47b20]">Home</RouterLink>
        <RouterLink to="/menu" class="block py-1 text-gray-700">Menu</RouterLink>
        <RouterLink to="/booking" class="block py-1 text-gray-700">Table Booking</RouterLink>
        <RouterLink to="/delivery" class="block py-1 text-gray-700">Home Delivery</RouterLink>
        <RouterLink to="/party-booking" class="block py-1 text-gray-700">Party Booking</RouterLink>
        <RouterLink to="/offers" class="block py-1 text-gray-700">Offers</RouterLink>
        <RouterLink to="/contact" class="block py-1 text-gray-700">Contact</RouterLink>
        <RouterLink to="/login" class="block py-1 text-gray-700 border-t pt-2">Staff Portal</RouterLink>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10 sm:py-16">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div class="lg:col-span-7 space-y-6">
          <div class="inline-flex items-center gap-2 rounded-full bg-orange-100 px-3.5 py-1 text-xs font-bold text-[#f47b20]">
            <Sparkles :size="14" /> {{ restaurant.tagline }}
          </div>
          <h1 class="font-heading text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-gray-900 leading-tight">
            Craving Good Food? <br />
            <span class="text-[#f47b20]">We've Got You Covered.</span>
          </h1>
          <p class="text-sm sm:text-base text-gray-600 max-w-xl leading-relaxed">
            {{ restaurant.description }}
          </p>

          <div class="flex flex-wrap items-center gap-3.5 pt-2">
            <RouterLink
              to="/menu"
              class="inline-flex items-center gap-2 rounded-xl bg-[#f47b20] px-6 py-3.5 text-xs font-bold text-white shadow-lg shadow-orange-500/20 transition hover:bg-[#d9630f]"
            >
              <ShoppingBag :size="16" /> Browse Menu
            </RouterLink>
            <RouterLink
              to="/booking"
              class="inline-flex items-center gap-2 rounded-xl border border-gray-300 bg-white px-6 py-3.5 text-xs font-bold text-gray-800 shadow-sm transition hover:bg-gray-50"
            >
              <CalendarDays :size="16" /> Book a Table
            </RouterLink>
          </div>
        </div>

        <div class="lg:col-span-5 relative">
          <div class="relative overflow-hidden rounded-3xl shadow-2xl border-4 border-white">
            <img
              :src="restaurant.heroImage"
              alt="Gourmet Dining"
              class="h-[360px] sm:h-[420px] w-full object-cover transition-transform duration-700 hover:scale-105"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Services Grid -->
    <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <RouterLink
          v-for="srv in services"
          :key="srv.title"
          :to="srv.link"
          class="p-5 rounded-2xl bg-white border border-gray-200 shadow-sm transition hover:shadow-md hover:border-orange-300 group"
        >
          <div class="h-10 w-10 rounded-xl bg-orange-50 flex items-center justify-center text-[#f47b20] mb-3 group-hover:scale-110 transition">
            <component :is="srv.icon" :size="20" />
          </div>
          <h3 class="font-bold text-sm text-gray-900">{{ srv.title }}</h3>
          <p class="text-[11px] text-gray-500 mt-0.5">{{ srv.description }}</p>
        </RouterLink>
      </div>
    </section>

    <!-- Popular Menu Dishes Preview -->
    <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="flex items-center justify-between mb-6">
        <div>
          <span class="text-[10px] font-bold uppercase tracking-wider text-[#f47b20]">Fresh & Delicious</span>
          <h2 class="font-heading text-2xl sm:text-3xl font-bold text-gray-900">Featured Gourmet Dishes</h2>
        </div>
        <RouterLink to="/menu" class="flex items-center gap-1 text-xs font-bold text-[#f47b20] hover:underline">
          View All Menu <ArrowRight :size="14" />
        </RouterLink>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div
          v-for="dish in menuPreview"
          :key="dish.name"
          class="p-3.5 rounded-2xl bg-white border border-gray-200 shadow-sm hover:shadow-md transition flex flex-col justify-between"
        >
          <div>
            <img :src="dish.image" :alt="dish.name" class="h-32 w-full object-cover rounded-xl mb-3" />
            <h4 class="font-bold text-xs text-gray-900 line-clamp-1">{{ dish.name }}</h4>
          </div>
          <div class="mt-3 flex items-center justify-between border-t border-gray-100 pt-2.5">
            <span class="font-bold text-sm text-[#f47b20]">₹{{ dish.price }}</span>
            <RouterLink to="/menu" class="rounded-md bg-gray-900 px-2.5 py-1 text-[10px] font-bold text-white hover:bg-[#f47b20]">
              + Add
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
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
  Menu,
  X,
  Sparkles,
  MapPin,
} from 'lucide-vue-next'
import { restroHandler } from '../services/api'

const mobileMenuOpen = ref(false)

const restaurant = ref({
  name: 'SHP',
  tagline: 'Good Food Great Moments',
  description: 'Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.',
  heroImage: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80',
})

const services = [
  { icon: CalendarDays, title: 'Table Booking', description: 'Reserve table in advance', link: '/booking' },
  { icon: Truck, title: 'Home Delivery', description: 'Hot & fresh food delivered', link: '/delivery' },
  { icon: UsersRound, title: 'Party / Celebration', description: 'Celebrate special moments', link: '/party-booking' },
  { icon: MapPin, title: 'Order Tracking', description: 'Track in real-time', link: '/delivery' },
]

const menuPreview = ref([
  { name: 'Truffle Mushroom Pizza', price: 349, image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=300&q=80' },
  { name: 'Artisan Smash Burger', price: 279, image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=300&q=80' },
  { name: 'Spicy Schezwan Noodles', price: 249, image: 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=300&q=80' },
  { name: 'Burrata Margherita Pizza', price: 389, image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=300&q=80' },
  { name: 'Dum Pukht Veg Biryani', price: 299, image: 'https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=300&q=80' },
])

onMounted(async () => {
  try {
    const restData = await restroHandler.restaurants.getCurrent()
    if (restData) {
      restaurant.value = {
        name: restData.name || 'SHP',
        tagline: restData.tagline || 'Good Food Great Moments',
        description: restData.description || 'Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.',
        heroImage: restData.hero_image || 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80',
      }
    }
  } catch {}

  try {
    const dishes = await restroHandler.menu.list()
    if (Array.isArray(dishes) && dishes.length > 0) {
      menuPreview.value = dishes.slice(0, 5).map((d) => ({
        name: d.name,
        price: d.price,
        image: d.image || 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=300&q=80',
      }))
    }
  } catch {
    // Keep defaults
  }
})
</script>

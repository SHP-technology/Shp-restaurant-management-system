<template>
  <footer class="bg-slate-50 text-slate-600 pt-16 pb-12 border-t border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-slate-200">
        <!-- Brand & About -->
        <div class="lg:col-span-2 space-y-4">
          <RouterLink to="/" class="flex items-center gap-2.5 group">
            <div class="w-10 h-10 rounded-xl bg-linear-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white font-bold text-xl shadow-md shadow-orange-500/20 group-hover:scale-105 transition-transform">
              🍽️
            </div>
            <div>
              <div class="font-heading font-extrabold text-xl text-slate-900 tracking-tight">
                SHP <span class="text-orange-600">RESTRO</span>
              </div>
              <div class="text-[10px] text-slate-500 font-medium tracking-wider uppercase">
                Gourmet Dining & Celebration Hub
              </div>
            </div>
          </RouterLink>
          <p class="text-sm text-slate-600 leading-relaxed max-w-sm">
            Crafting culinary excellence since 2020. Serving authentic royal Indian delicacies, gourmet sizzlers, wood-fired delights, and handcrafted desserts.
          </p>
          <div class="flex flex-wrap items-center gap-2.5 pt-2">
            <span class="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-700 text-xs font-semibold px-3 py-1 rounded-full border border-emerald-200">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Kitchen Open Now
            </span>
            <span class="text-xs text-slate-600 bg-white border border-slate-200 px-2.5 py-1 rounded-full shadow-2xs">
              FSSAI Lic: 10021011000452
            </span>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="space-y-3">
          <h4 class="text-slate-900 font-bold text-sm tracking-wider uppercase font-heading">Explore</h4>
          <ul class="space-y-2.5 text-sm text-slate-600">
            <li><RouterLink to="/menu" class="hover:text-orange-600 transition-colors inline-block py-0.5">Dine-In Menu</RouterLink></li>
            <li><RouterLink to="/delivery" class="hover:text-orange-600 transition-colors inline-block py-0.5">Online Delivery</RouterLink></li>
            <li><RouterLink to="/booking" class="hover:text-orange-600 transition-colors inline-block py-0.5">Reserve a Table</RouterLink></li>
            <li><RouterLink to="/party-booking" class="hover:text-orange-600 transition-colors inline-block py-0.5">Party & Event Hall</RouterLink></li>
            <li><RouterLink to="/offers" class="hover:text-orange-600 transition-colors inline-block py-0.5">Special Deals</RouterLink></li>
          </ul>
        </div>

        <!-- Working Hours & Outlets -->
        <div class="space-y-3">
          <h4 class="text-slate-900 font-bold text-sm tracking-wider uppercase font-heading">Timings</h4>
          <div class="text-sm text-slate-600 space-y-2">
            <div class="text-slate-900 font-medium flex items-center gap-1.5">
              <span>📅</span> Monday – Sunday
            </div>
            <div class="text-xs bg-white p-3 rounded-xl border border-slate-200 shadow-2xs space-y-1.5">
              <div class="flex justify-between">
                <span class="text-slate-500">Lunch:</span>
                <span class="text-slate-800 font-semibold">11:00 AM – 04:00 PM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Dinner:</span>
                <span class="text-slate-800 font-semibold">06:30 PM – 11:30 PM</span>
              </div>
            </div>
            <div class="text-orange-600 text-xs pt-0.5 font-semibold flex items-center gap-1">
              <span>🛵</span> Doorstep delivery runs all day
            </div>
          </div>
        </div>

        <!-- Contact & Support -->
        <div class="space-y-3">
          <h4 class="text-slate-900 font-bold text-sm tracking-wider uppercase font-heading">Visit & Contact</h4>
          <div class="text-sm text-slate-600 space-y-2.5">
            <p class="leading-snug text-xs sm:text-sm text-slate-600">
              📍 Plot 14, Main Boulevard, Civil Lines, City - 110054
            </p>
            <p>
              <a href="tel:+919876543210" class="text-slate-900 hover:text-orange-600 font-semibold transition-colors flex items-center gap-1.5">
                <span>📞</span> +91 98765 43210
              </a>
            </p>
            <p>
              <a href="mailto:contact@shprestaurant.com" class="text-slate-600 hover:text-orange-600 transition-colors text-xs flex items-center gap-1.5">
                <span>✉️</span> contact@shprestaurant.com
              </a>
            </p>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <div>
          © 2026 SHP Restro. All Rights Reserved. Powered by SHP Restaurant OS.
        </div>
        <div class="flex flex-wrap items-center gap-5 sm:gap-6">
          <RouterLink to="/contact" class="hover:text-slate-900 transition-colors">Privacy Policy</RouterLink>
          <RouterLink to="/contact" class="hover:text-slate-900 transition-colors">Terms of Service</RouterLink>
          <RouterLink to="/login" class="text-slate-700 hover:text-orange-600 transition-colors font-semibold flex items-center gap-1">
            <span>Staff Portal →</span>
          </RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

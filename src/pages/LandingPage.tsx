import {
  CalendarDays,
  ChevronRight,
  MapPin,
  ShoppingBag,
  Truck,
  UsersRound,
  ArrowRight,
  Menu as MenuIcon,
  X as CloseIcon,
  Percent,
  CreditCard,
  Building2,
  Smile,
  Search,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'

const fallbackData = {
  restaurant: {
    name: 'SHP',
    tagline: 'Good Food Great Moments',
    description:
      'Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.',
    heroImage:
      'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80',
  },

  categories: [
    {
      id: 1,
      name: 'Pizza',
      image:
        'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 2,
      name: 'Burgers',
      image:
        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 3,
      name: 'Chinese',
      image:
        'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 4,
      name: 'Beverages',
      image:
        'https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=500&q=80',
    },
    {
      id: 5,
      name: 'Desserts',
      image:
        'https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=500&q=80',
    },
  ],

  menuPreview: [
    { name: 'Margherita Pizza', price: 249, image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=150&q=80' },
    { name: 'Veg Loaded Burger', price: 199, image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=150&q=80' },
    { name: 'Paneer Chinese', price: 299, image: 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=150&q=80' },
    { name: 'Paneer Pizza', price: 349, image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=150&q=80' },
    { name: 'Veg Biryani', price: 249, image: 'https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=150&q=80' },
  ],
}

const services = [
  {
    icon: CalendarDays,
    title: 'Table Booking',
    description: 'Reserve your table',
    action: 'in advance',
    link: '/booking',
  },
  {
    icon: Truck,
    title: 'Home Delivery',
    description: 'Hot & fresh food',
    action: 'delivered',
    link: '/delivery',
  },
  {
    icon: UsersRound,
    title: 'Party / Celebration',
    description: 'Celebrate your special',
    action: 'days with us',
    link: '/party-booking',
  },
  {
    icon: MapPin,
    title: 'Order Tracking',
    description: 'Track your order',
    action: 'in real-time',
    link: '/delivery',
  },
]

export function LandingPage() {
  const [data] = useState(fallbackData)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-[#f7f5f0] text-[#1a1917] font-sans">
      {/* Top Banner Title - Matching Image Header */}
      <div className="bg-[#f7f5f0] border-b border-gray-200 py-2.5 text-center text-xs font-bold uppercase tracking-wider text-gray-600">
        <span className="inline-flex items-center gap-1.5">
          🌐 CUSTOMER WEBSITE • For Ordering, Table Booking, Party Booking & More
        </span>
      </div>

      {/* Main Navbar */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-2.5">
            <img src="/logo.png" alt="SHP Restaurant Logo" className="h-9 w-9 rounded-lg object-cover shadow-sm" />
            <span className="font-heading text-2xl font-black tracking-tight text-gray-900">
              SHP<span className="text-[#f47b20]">.</span>
            </span>
          </Link>

          {/* Desktop Links */}
          <nav className="hidden md:flex items-center gap-6 text-xs font-semibold text-gray-700">
            <Link to="/" className="text-[#f47b20] font-bold">Home</Link>
            <Link to="/menu" className="hover:text-[#f47b20] transition">Menu</Link>
            <Link to="/booking" className="hover:text-[#f47b20] transition">Book Table</Link>
            <Link to="/delivery" className="hover:text-[#f47b20] transition">Delivery</Link>
            <Link to="/party-booking" className="hover:text-[#f47b20] transition">Party Booking</Link>
            <Link to="/offers" className="hover:text-[#f47b20] transition">Offers</Link>
            <Link to="/contact" className="hover:text-[#f47b20] transition">Contact</Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-3">
            <Link to="/menu" className="relative flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 text-gray-800">
              <ShoppingBag size={16} />
              <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-[#f47b20] text-[9px] font-bold text-white">
                0
              </span>
            </Link>

            <Link
              to="/login"
              className="rounded-md bg-black px-4 py-1.5 text-xs font-bold text-white hover:bg-gray-800 transition"
            >
              Login
            </Link>

            <Link
              to="/admin"
              className="hidden lg:inline-flex items-center gap-1 rounded-md border border-gray-300 bg-gray-50 px-3 py-1.5 text-xs font-bold text-gray-800 hover:border-[#f47b20] hover:text-[#f47b20]"
            >
              Outlet Panel <ArrowRight size={12} />
            </Link>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="flex h-8 w-8 items-center justify-center rounded-md bg-gray-100 text-gray-800 md:hidden"
            >
              {mobileMenuOpen ? <CloseIcon size={18} /> : <MenuIcon size={18} />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Nav */}
        {mobileMenuOpen && (
          <nav className="border-t border-gray-200 bg-white px-6 py-4 md:hidden space-y-3 text-xs font-semibold">
            <Link to="/" onClick={() => setMobileMenuOpen(false)} className="block text-[#f47b20] font-bold">Home</Link>
            <Link to="/menu" onClick={() => setMobileMenuOpen(false)} className="block text-gray-700">Menu</Link>
            <Link to="/booking" onClick={() => setMobileMenuOpen(false)} className="block text-gray-700">Book Table</Link>
            <Link to="/delivery" onClick={() => setMobileMenuOpen(false)} className="block text-gray-700">Delivery</Link>
            <Link to="/party-booking" onClick={() => setMobileMenuOpen(false)} className="block text-gray-700">Party Booking</Link>
            <Link to="/admin" onClick={() => setMobileMenuOpen(false)} className="block text-[#f47b20] font-bold pt-2 border-t">Outlet Panel (Staff)</Link>
          </nav>
        )}
      </header>

      {/* HERO BANNER - Exact layout matching Image */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 pt-6">
        <div className="relative overflow-hidden rounded-2xl bg-[#0f0e0d] p-6 sm:p-12 lg:p-14 text-white shadow-xl">
          <div className="grid items-center gap-8 lg:grid-cols-12">
            <div className="lg:col-span-7 space-y-4">
              <h1 className="font-heading text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.02]">
                Good Food<br />
                <span className="text-[#f47b20]">Great Moments</span>
              </h1>

              <p className="max-w-md text-xs sm:text-sm text-gray-300 leading-relaxed">
                {data.restaurant.description}
              </p>

              <div className="pt-2 flex flex-wrap items-center gap-3">
                <Link
                  to="/menu"
                  className="rounded-md bg-[#f47b20] px-6 py-2.5 text-xs font-bold text-white shadow-md hover:bg-[#d9630f] transition"
                >
                  Order Now
                </Link>

                <Link
                  to="/booking"
                  className="rounded-md border border-white/80 px-6 py-2.5 text-xs font-bold text-white hover:bg-white/10 transition"
                >
                  Book a Table
                </Link>
              </div>
            </div>

            <div className="lg:col-span-5 flex justify-center">
              <div className="relative h-64 sm:h-72 w-full max-w-md overflow-hidden rounded-2xl border border-white/10 shadow-2xl">
                <img
                  src={data.restaurant.heroImage}
                  alt="Delicious Food Dish"
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SERVICES FLOATING ROW - Exact 4 columns matching Image */}
      <section className="relative z-10 mx-auto max-w-[1240px] px-4 sm:px-6 -mt-6">
        <div className="grid grid-cols-2 sm:grid-cols-4 rounded-xl border border-gray-200 bg-white p-2 sm:p-4 shadow-md gap-2 sm:gap-4">
          {services.map((service) => {
            const Icon = service.icon
            return (
              <Link
                key={service.title}
                to={service.link}
                className="group flex flex-col items-center justify-center p-3 text-center rounded-lg border border-gray-100 hover:border-orange-200 hover:bg-orange-50/50 transition"
              >
                <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-orange-100 text-[#f47b20]">
                  <Icon size={20} />
                </div>
                <h3 className="text-xs sm:text-sm font-bold text-gray-900 group-hover:text-[#f47b20]">
                  {service.title}
                </h3>
                <p className="mt-0.5 text-[10px] text-gray-500 leading-tight">
                  {service.description}<br />{service.action}
                </p>
              </Link>
            )
          })}
        </div>
      </section>

      {/* POPULAR CATEGORIES - Matching 5 grid cards in Image */}
      <section className="mx-auto max-w-[1240px] px-4 sm:px-6 py-10">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-heading text-lg sm:text-xl font-bold tracking-tight text-gray-900">
            Popular Categories
          </h2>
          <Link to="/menu" className="flex items-center gap-1 text-xs font-bold text-[#f47b20] hover:underline">
            View All <ChevronRight size={13} />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {data.categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/menu?category=${encodeURIComponent(cat.name)}`}
              className="group relative h-28 sm:h-32 overflow-hidden rounded-lg bg-black shadow-sm"
            >
              <img
                src={cat.image}
                alt={cat.name}
                className="h-full w-full object-cover opacity-80 transition duration-300 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
              <span className="absolute bottom-2.5 left-2.5 text-xs font-bold text-white">
                {cat.name}
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* WEBSITE PAGES PREVIEW SECTION - Exact matching preview boxes in lower half of image */}
      <section className="border-t border-gray-200 bg-[#efece6] py-12 px-4 sm:px-6">
        <h2 className="text-center font-heading text-xs font-bold uppercase tracking-widest text-gray-600 mb-8">
          WEBSITE PAGES PREVIEW
        </h2>

        <div className="mx-auto grid max-w-[1240px] gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          {/* 1. MENU PAGE PREVIEW */}
          <div className="overflow-hidden rounded-xl border border-gray-300 bg-white shadow-sm flex flex-col">
            <div className="bg-gray-100 py-2 text-center text-[11px] font-bold text-gray-600 border-b border-gray-200">
              MENU PAGE
            </div>
            <div className="p-3.5 space-y-3 flex-1 flex flex-col">
              <div className="flex items-center gap-2 border-b pb-2">
                <Search size={14} className="text-gray-400" />
                <span className="text-xs text-gray-400">Search food items...</span>
              </div>

              <div className="flex gap-2 text-[11px] font-bold border-b pb-2 text-gray-600 overflow-x-auto">
                <span className="text-[#f47b20]">All</span>
                <span>Pizza</span>
                <span>Burgers</span>
                <span>Indian</span>
                <span>Chinese</span>
              </div>

              <div className="space-y-2.5 flex-1">
                {data.menuPreview.slice(0, 4).map((item) => (
                  <div key={item.name} className="flex items-center justify-between text-xs border-b border-gray-100 pb-2">
                    <div className="flex items-center gap-2">
                      <img src={item.image} alt={item.name} className="h-9 w-9 rounded object-cover" />
                      <div>
                        <p className="font-bold text-gray-800 text-[11px]">{item.name}</p>
                        <p className="text-[10px] text-[#f47b20] font-semibold">₹{item.price}</p>
                      </div>
                    </div>
                    <button className="rounded bg-[#f47b20] px-2 py-1 text-[10px] font-bold text-white">
                      ADD
                    </button>
                  </div>
                ))}
              </div>

              <Link to="/menu" className="block w-full text-center rounded bg-[#f47b20] py-2 text-xs font-bold text-white mt-auto">
                Open Full Menu Page
              </Link>
            </div>
          </div>

          {/* 2. TABLE BOOKING PAGE PREVIEW */}
          <div className="overflow-hidden rounded-xl border border-gray-300 bg-white shadow-sm flex flex-col">
            <div className="bg-gray-100 py-2 text-center text-[11px] font-bold text-gray-600 border-b border-gray-200">
              TABLE BOOKING PAGE
            </div>
            <div className="p-3.5 space-y-2.5 text-xs flex-1 flex flex-col">
              <p className="font-bold text-gray-900 flex items-center gap-1 text-xs">
                <CalendarDays size={14} className="text-[#f47b20]" /> Book Your Table
              </p>

              <div>
                <label className="text-[10px] text-gray-500 font-semibold block">Restaurant</label>
                <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                  SHP Restaurant, Civil Lines
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Date</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    28 May 2025
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Time</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    7:30 PM
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Persons</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    4 People
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Area</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    Indoor
                  </div>
                </div>
              </div>

              <Link to="/booking" className="block w-full text-center rounded bg-[#f47b20] py-2 text-xs font-bold text-white mt-auto">
                Check Availability
              </Link>

              <img
                src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80"
                alt="Restaurant interior"
                className="h-14 w-full object-cover rounded mt-2"
              />
            </div>
          </div>

          {/* 3. PARTY BOOKING PAGE PREVIEW */}
          <div className="overflow-hidden rounded-xl border border-gray-300 bg-white shadow-sm flex flex-col">
            <div className="bg-gray-100 py-2 text-center text-[11px] font-bold text-gray-600 border-b border-gray-200">
              PARTY BOOKING PAGE
            </div>
            <div className="p-3.5 space-y-2.5 text-xs flex-1 flex flex-col">
              <p className="font-bold text-gray-900 flex items-center gap-1 text-xs">
                <UsersRound size={14} className="text-[#f47b20]" /> Plan Your Celebration
              </p>
              <p className="text-[10px] text-gray-500">Make your special moments memorable with us.</p>

              <div>
                <label className="text-[10px] text-gray-500 font-semibold block">Occasion</label>
                <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                  Birthday Bash
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Date</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    05 June 2025
                  </div>
                </div>
                <div>
                  <label className="text-[10px] text-gray-500 font-semibold block">Guests</label>
                  <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                    20 People
                  </div>
                </div>
              </div>

              <div>
                <label className="text-[10px] text-gray-500 font-semibold block">Requirements</label>
                <div className="rounded border border-gray-200 px-2 py-1.5 text-[11px] text-gray-700 bg-gray-50">
                  Decoration, Cake, Music
                </div>
              </div>

              <Link to="/party-booking" className="block w-full text-center rounded bg-[#f47b20] py-2 text-xs font-bold text-white mt-auto">
                Send Request
              </Link>
            </div>
          </div>

          {/* 4. ORDER TRACKING PAGE PREVIEW */}
          <div className="overflow-hidden rounded-xl border border-gray-300 bg-white shadow-sm flex flex-col">
            <div className="bg-gray-100 py-2 text-center text-[11px] font-bold text-gray-600 border-b border-gray-200">
              ORDER TRACKING PAGE
            </div>
            <div className="p-3.5 space-y-3 text-xs flex-1 flex flex-col">
              <p className="font-bold text-gray-900 flex items-center gap-1 text-xs">
                <Truck size={14} className="text-[#f47b20]" /> Track Your Order
              </p>
              <p className="text-[10px] text-gray-500 font-bold">Order ID: #1257</p>

              <div className="space-y-2 text-[11px] border-l-2 border-orange-400 pl-3">
                <div className="flex justify-between items-center text-emerald-700 font-bold">
                  <span>● Order Confirmed</span>
                  <span className="text-[9px] text-gray-400">10:00 AM</span>
                </div>
                <div className="flex justify-between items-center text-[#f47b20] font-bold">
                  <span>● Preparing</span>
                  <span className="text-[9px] text-gray-400">10:10 AM</span>
                </div>
                <div className="flex justify-between items-center text-gray-400">
                  <span>○ Out for Delivery</span>
                  <span className="text-[9px] text-gray-400">10:25 AM</span>
                </div>
              </div>

              <Link to="/delivery" className="block w-full text-center rounded bg-[#f47b20] py-2 text-xs font-bold text-white mt-auto">
                Track Live Order
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* KEY FEATURES BAR - Exact matching bottom bar in Image */}
      <section className="border-t border-gray-200 bg-white py-6 px-4 sm:px-6">
        <div className="mx-auto max-w-7xl">
          <p className="text-center font-heading text-xs font-bold uppercase tracking-widest text-gray-500 mb-6">
            KEY FEATURES
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-4 text-center">
            {[
              { label: 'Table Booking', sub: '(Real-time Availability)', icon: CalendarDays },
              { label: 'Home Delivery', sub: '(Tracking & Notifications)', icon: Truck },
              { label: 'Party / Celebration', sub: 'Booking', icon: UsersRound },
              { label: 'Multi Outlet', sub: 'Management', icon: Building2 },
              { label: 'Live Order', sub: 'Tracking', icon: MapPin },
              { label: 'Offers &', sub: 'Discounts', icon: Percent },
              { label: 'Secure Payments', sub: '(Online / COD)', icon: CreditCard },
              { label: 'User Friendly', sub: 'UI / UX', icon: Smile },
            ].map((item) => {
              const Icon = item.icon
              return (
                <div key={item.label} className="flex flex-col items-center text-center">
                  <div className="mb-1.5 flex h-9 w-9 items-center justify-center rounded-lg bg-orange-50 text-[#f47b20]">
                    <Icon size={18} />
                  </div>
                  <p className="text-[11px] font-bold text-gray-900 leading-tight">{item.label}</p>
                  <p className="text-[9px] text-gray-500 leading-tight">{item.sub}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-[#0b0b0b] py-6 text-white">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 sm:flex-row">
          <Link to="/" className="font-heading text-xl font-bold text-white">
            {data.restaurant.name}<span className="text-[#f47b20]">.</span>
          </Link>
          <p className="text-xs text-gray-400">Good food for great moments. All rights reserved.</p>
          <div className="flex items-center gap-6 text-xs text-gray-300 font-medium">
            <Link to="/menu" className="hover:text-[#f47b20]">Menu</Link>
            <Link to="/booking" className="hover:text-[#f47b20]">Book Table</Link>
            <Link to="/admin" className="hover:text-[#f47b20]">Outlet Panel</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Truck, MapPin, Clock, ShieldCheck } from 'lucide-react'

export function DeliveryPage() {
  const [address, setAddress] = useState('Flat 402, Sunset Towers, Civil Lines')
  const [instructions, setInstructions] = useState('Leave at door & ring bell')
  const [orderPlaced, setOrderPlaced] = useState(false)

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Top Header */}
      <header className="border-b border-gray-200 bg-white px-4 sm:px-6 py-3.5 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <Link to="/" className="flex items-center gap-1.5 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
            <ArrowLeft size={16} /> Home
          </Link>
          <span className="font-heading text-base sm:text-lg font-bold text-gray-900">Home Delivery</span>
          <div className="w-12 sm:w-16" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 sm:px-6 py-8 sm:py-12">
        <div className="mb-8 sm:mb-10 text-center">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-orange-100 px-3.5 py-1 text-xs font-bold text-[#f47b20]">
            <Truck size={14} /> Doorstep Delivery
          </span>
          <h1 className="mt-2.5 font-heading text-3xl sm:text-4xl font-extrabold tracking-tight text-gray-900">
            Order Gourmet Delivery
          </h1>
          <p className="mt-1.5 text-xs sm:text-sm text-gray-500 max-w-md mx-auto">
            Fresh, hot food delivered directly to your doorstep in 30-40 minutes.
          </p>
        </div>

        {orderPlaced ? (
          <div className="rounded-2xl border border-gray-200 bg-white p-5 sm:p-8 shadow-lg max-w-3xl mx-auto">
            <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-gray-100 pb-4">
              <div>
                <p className="text-[10px] uppercase tracking-wider text-[#f47b20] font-bold">Live Status</p>
                <h2 className="text-lg sm:text-xl font-bold text-gray-900 mt-0.5">Order #SHP-9482 is in Kitchen!</h2>
              </div>
              <div className="flex items-center gap-1.5 rounded-full bg-orange-50 px-3 py-1.5 text-xs font-bold text-[#f47b20] border border-orange-200 w-fit">
                <Clock size={14} /> Est. Delivery: 28 mins
              </div>
            </div>

            {/* Live Progress Bar - Responsive Grid */}
            <div className="my-6 grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-[11px]">
              {[
                { label: 'Order Confirmed', done: true },
                { label: 'Preparing Food', done: true },
                { label: 'Out for Delivery', done: false },
                { label: 'Delivered', done: false },
              ].map((step, idx) => (
                <div key={step.label} className="space-y-1.5">
                  <div
                    className={`h-2 rounded-full ${
                      step.done ? 'bg-[#f47b20]' : 'bg-gray-200'
                    }`}
                  />
                  <p className={step.done ? 'font-bold text-gray-900' : 'text-gray-400'}>
                    {idx + 1}. {step.label}
                  </p>
                </div>
              ))}
            </div>

            <div className="rounded-xl border border-gray-200 bg-gray-50 p-4 space-y-2 text-xs">
              <div className="flex items-center gap-2 text-gray-700">
                <MapPin size={16} className="text-[#f47b20] shrink-0" />
                <span>Delivering to: <strong className="text-gray-900">{address}</strong></span>
              </div>
              <div className="flex items-center gap-2 text-gray-700">
                <ShieldCheck size={16} className="text-emerald-600 shrink-0" />
                <span>Heat-sealed hygienic packaging verified</span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <Link
                to="/menu"
                className="inline-flex items-center gap-2 rounded-md bg-[#f47b20] px-6 py-2.5 text-xs font-bold text-white transition hover:bg-[#d9630f]"
              >
                Browse Menu Again
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Delivery Details Form */}
            <div className="lg:col-span-2 space-y-5 rounded-2xl border border-gray-200 bg-white p-5 sm:p-6 shadow-sm">
              <h2 className="text-base sm:text-lg font-bold text-gray-900 flex items-center gap-2">
                <MapPin size={18} className="text-[#f47b20]" /> Delivery Address & Contact
              </h2>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                  Delivery Address
                </label>
                <textarea
                  rows={2}
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="w-full rounded-md border border-gray-300 bg-white p-3 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold uppercase tracking-wider text-gray-700 mb-1.5">
                  Delivery Instructions (Optional)
                </label>
                <input
                  type="text"
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  className="w-full rounded-md border border-gray-300 bg-white px-3.5 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>

              <div className="rounded-xl border border-orange-200 bg-orange-50/50 p-3.5 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <Clock size={18} className="text-[#f47b20] shrink-0" />
                  <div>
                    <p className="text-xs font-bold text-gray-900">Estimated Delivery Time</p>
                    <p className="text-[10px] text-gray-500">30 - 45 Minutes from confirmation</p>
                  </div>
                </div>
                <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-700 shrink-0">
                  FREE
                </span>
              </div>

              <button
                onClick={() => setOrderPlaced(true)}
                className="w-full rounded-md bg-[#f47b20] py-3 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f]"
              >
                Place Delivery Order
              </button>
            </div>

            {/* Order Summary Sidebar */}
            <div className="space-y-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm h-fit">
              <h3 className="text-base font-bold text-gray-900">Order Summary</h3>
              <div className="space-y-2.5 text-xs border-b border-gray-100 pb-3.5">
                <div className="flex justify-between text-gray-700">
                  <span>1x Truffle Mushroom Pizza</span>
                  <span className="font-bold">₹349</span>
                </div>
                <div className="flex justify-between text-gray-700">
                  <span>1x Matcha Citrus Sparkler</span>
                  <span className="font-bold">₹169</span>
                </div>
              </div>

              <div className="space-y-2 text-[11px] text-gray-500 border-b border-gray-100 pb-3.5">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span className="text-gray-800 font-medium">₹518</span>
                </div>
                <div className="flex justify-between">
                  <span>Taxes & Packaging</span>
                  <span className="text-gray-800 font-medium">₹36</span>
                </div>
                <div className="flex justify-between">
                  <span>Delivery Charge</span>
                  <span className="text-emerald-600 font-bold">FREE</span>
                </div>
              </div>

              <div className="flex justify-between text-base font-bold text-gray-900 pt-0.5">
                <span>Grand Total</span>
                <span className="text-[#f47b20]">₹554</span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Users, Gift, Cake, Sparkles, CheckCircle2 } from 'lucide-react'

export function PartyBookingPage() {
  const [occasion, setOccasion] = useState('Birthday Celebration')
  const [guestCount, setGuestCount] = useState('25-50 Guests')
  const [date, setDate] = useState('2026-10-15')
  const [submitted, setSubmitted] = useState(false)

  const occasions = [
    { title: 'Birthday Bash', icon: Cake, desc: 'Custom cake, balloon decor & music setup' },
    { title: 'Corporate Gala', icon: Users, desc: 'Private dining, podium & cocktail service' },
    { title: 'Anniversary & Party', icon: Gift, desc: 'Candlelight setup & live music' },
    { title: 'Custom Event', icon: Sparkles, desc: 'Bespoke menu & complete venue booking' },
  ]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-[#fffdf9] text-[#1d211e]">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-[#f47b20] transition">
            <ArrowLeft size={16} /> Home
          </Link>
          <span className="font-heading text-lg font-bold text-gray-900">Party Booking</span>
          <div className="w-16" />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-12">
        <div className="mb-10 text-center">
          <span className="inline-flex items-center gap-2 rounded-full bg-orange-100 px-4 py-1.5 text-xs font-bold text-[#f47b20]">
            <Sparkles size={14} /> Memorable Gatherings
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Host Your Event with Us
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-gray-500">
            From birthday bashes to corporate dinners. Tailored catering and event management.
          </p>
        </div>

        {submitted ? (
          <div className="rounded-2xl border border-gray-200 bg-white p-10 text-center shadow-lg max-w-xl mx-auto">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
              <CheckCircle2 size={40} />
            </div>
            <h2 className="mt-6 text-2xl font-bold text-gray-900">Inquiry Submitted!</h2>
            <p className="mt-3 text-sm text-gray-600">
              Thank you for booking your <span className="text-[#f47b20] font-bold">{occasion}</span> on{' '}
              <span className="text-[#f47b20] font-bold">{date}</span>.
            </p>
            <p className="mt-2 text-xs text-gray-500">
              Our event manager will contact you within 2 hours to confirm menu and decor details.
            </p>
            <div className="mt-8">
              <Link
                to="/"
                className="rounded-md bg-[#f47b20] px-6 py-3 text-xs font-bold text-white transition hover:bg-[#d9630f]"
              >
                Return to Home
              </Link>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
            {/* Occasion cards */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-4 block">Select Occasion Type</label>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {occasions.map((occ) => {
                  const Icon = occ.icon
                  const isSelected = occasion === occ.title
                  return (
                    <div
                      key={occ.title}
                      onClick={() => setOccasion(occ.title)}
                      className={`cursor-pointer rounded-xl border p-5 transition ${
                        isSelected
                          ? 'border-[#f47b20] bg-orange-50/70 shadow-sm'
                          : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                      }`}
                    >
                      <Icon size={24} className={`mb-3 ${isSelected ? 'text-[#f47b20]' : 'text-gray-400'}`} />
                      <p className="font-bold text-gray-900 text-xs">{occ.title}</p>
                      <p className="mt-1 text-[11px] text-gray-500 leading-relaxed">{occ.desc}</p>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Inputs */}
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
                  Expected Guests
                </label>
                <select
                  value={guestCount}
                  onChange={(e) => setGuestCount(e.target.value)}
                  className="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                >
                  <option>10 - 25 Guests</option>
                  <option>25 - 50 Guests</option>
                  <option>50 - 100 Guests</option>
                  <option>100+ Exclusive Hall Booking</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
                  Event Date
                </label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
                Contact Person Name & Phone Number
              </label>
              <input
                type="text"
                required
                placeholder="Alex Morgan - +91 98765 43210"
                className="w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-xs text-gray-800 focus:border-[#f47b20] focus:outline-none"
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-md bg-[#f47b20] py-3.5 text-xs font-bold text-white shadow-md transition hover:bg-[#d9630f]"
            >
              Submit Party Booking Request
            </button>
          </form>
        )}
      </main>
    </div>
  )
}

import {
  CalendarDays,
  ChevronRight,
  MapPin,
  ShoppingBag,
  Truck,
  UsersRound,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const fallbackData = {
  restaurant: {
    name: "SHP",
    tagline: "Good Food Great Moments",
    description:
      "Delicious food, year after year — dine-in, delivery or celebration, we’ve got you covered.",
    heroImage:
      "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=1600&q=85",
  },

  categories: [
    {
      id: 1,
      name: "Pizza",
      image:
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 2,
      name: "Burgers",
      image:
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 3,
      name: "Chinese",
      image:
        "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 4,
      name: "Beverages",
      image:
        "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 5,
      name: "Desserts",
      image:
        "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=500&q=80",
    },
  ],

  menu: [
    {
      id: 1,
      name: "Margherita Pizza",
      price: 249,
      category: "Pizza",
      image:
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 2,
      name: "Veg Loaded Burger",
      price: 199,
      category: "Burgers",
      image:
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 3,
      name: "Paneer Chinese",
      price: 299,
      category: "Chinese",
      image:
        "https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 4,
      name: "Paneer Pizza",
      price: 349,
      category: "Pizza",
      image:
        "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=500&q=80",
    },
    {
      id: 5,
      name: "Veg Biryani",
      price: 249,
      category: "Chinese",
      image:
        "https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=500&q=80",
    },
  ],
};

const services = [
  {
    icon: CalendarDays,
    title: "Table Booking",
    description: "Reserve your table",
    action: "in advance",
    link: "/booking",
  },
  {
    icon: Truck,
    title: "Home Delivery",
    description: "Fresh & hot food",
    action: "delivered",
    link: "/delivery",
  },
  {
    icon: UsersRound,
    title: "Party / Celebration",
    description: "Celebrate with us",
    action: "your moments",
    link: "/party-booking",
  },
  {
    icon: MapPin,
    title: "Order Tracking",
    description: "Track your order",
    action: "in real-time",
    link: "/orders",
  },
];

export function LandingPage() {
  const [data, setData] = useState(fallbackData);

  useEffect(() => {
    const fetchHomeData = async () => {
      try {
        const response = await fetch(
          `${API_URL}/restaurant/home`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch homepage data");
        }

        const result = await response.json();

        setData({
          restaurant:
            result.restaurant || fallbackData.restaurant,

          categories:
            result.categories?.length
              ? result.categories
              : fallbackData.categories,

          menu:
            result.menu?.length
              ? result.menu
              : fallbackData.menu,
        });
      } catch (error) {
        console.error(
          "Homepage API error:",
          error
        );
      }
    };

    fetchHomeData();
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">

      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <header className="h-[54px] border-b border-gray-100 bg-white">

        <div className="mx-auto flex h-full max-w-[1400px] items-center px-4 sm:px-6 lg:px-8">

          {/* Logo */}

          <Link
            to="/"
            className="text-[21px] font-black tracking-[-1.5px]"
          >
            {data.restaurant.name}
            <span className="text-orange-500">.</span>
          </Link>

          {/* Navigation */}

          <nav className="ml-8 hidden items-center gap-5 md:flex lg:ml-10 lg:gap-6">

            <Link
              to="/"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Home
            </Link>

            <Link
              to="/menu"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Menu
            </Link>

            <Link
              to="/booking"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Book Table
            </Link>

            <Link
              to="/delivery"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Delivery
            </Link>

            <Link
              to="/party-booking"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Party Booking
            </Link>

            <Link
              to="/offers"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Offers
            </Link>

            <Link
              to="/contact"
              className="text-[11px] font-medium text-gray-700 transition hover:text-orange-500"
            >
              Contact
            </Link>

          </nav>

          {/* Right */}

          <div className="ml-auto flex items-center gap-4">

            <Link
              to="/cart"
              className="relative text-gray-800"
            >
              <ShoppingBag size={15} />

              <span className="absolute -right-2 -top-2 flex h-[14px] w-[14px] items-center justify-center rounded-full bg-orange-500 text-[8px] text-white">
                0
              </span>
            </Link>

            <Link
              to="/login"
              className="rounded-[4px] bg-black px-4 py-[7px] text-[10px] font-medium text-white"
            >
              Login
            </Link>

          </div>

        </div>

      </header>


      {/* =====================================================
          HERO
      ===================================================== */}

      <main>

        <section
          className="relative min-h-[285px] bg-cover bg-center"
          style={{
            backgroundImage: `url("${data.restaurant.heroImage}")`,
          }}
        >

          {/* Dark overlay */}

          <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/65 to-black/10" />

          {/* Content */}

          <div className="relative mx-auto flex min-h-[285px] max-w-[1400px] items-center px-6 sm:px-10 lg:px-12">

            <div className="max-w-[390px] text-white">

              <h1 className="text-[38px] font-extrabold leading-[0.98] tracking-[-1.8px] sm:text-[42px]">
                Good Food
                <br />
                Great Moments
              </h1>

              <p className="mt-4 max-w-[340px] text-[10px] leading-[1.55] text-gray-300 sm:text-[11px]">
                {data.restaurant.description}
              </p>

              <div className="mt-5 flex gap-2">

                <Link
                  to="/menu"
                  className="rounded-[4px] bg-orange-500 px-5 py-[9px] text-[10px] font-semibold text-white transition hover:bg-orange-600"
                >
                  Order Now
                </Link>

                <Link
                  to="/booking"
                  className="rounded-[4px] border border-white/80 px-5 py-[9px] text-[10px] font-semibold text-white transition hover:bg-white/10"
                >
                  Book a Table
                </Link>

              </div>

            </div>

          </div>

        </section>


        {/* =====================================================
            SERVICES
        ===================================================== */}

        <section className="relative z-10 mx-auto -mt-[17px] w-[calc(100%-32px)] max-w-[1250px] overflow-hidden rounded-[6px] bg-white shadow-[0_3px_18px_rgba(0,0,0,0.09)] sm:w-[calc(100%-60px)]">

          <div className="grid grid-cols-4">

            {services.map((service, index) => {

              const Icon = service.icon;

              return (
                <Link
                  key={service.title}
                  to={service.link}
                  className={`
                    flex min-h-[82px]
                    flex-col items-center
                    justify-center
                    border-gray-100
                    px-1 text-center
                    transition hover:bg-orange-50
                    ${index !== 3 ? "border-r" : ""}
                  `}
                >

                  <Icon
                    size={21}
                    strokeWidth={1.5}
                    className="mb-1 text-orange-500"
                  />

                  <h3 className="text-[8px] font-bold sm:text-[9px]">
                    {service.title}
                  </h3>

                  <p className="mt-[2px] text-[6px] leading-[1.4] text-gray-400 sm:text-[7px]">
                    {service.description}
                    <br />
                    {service.action}
                  </p>

                </Link>
              );

            })}

          </div>

        </section>


        {/* =====================================================
            POPULAR CATEGORIES
        ===================================================== */}

        <section className="mx-auto max-w-[1250px] px-5 pb-7 pt-7 sm:px-8 lg:px-10">

          <div className="mb-3 flex items-center justify-between">

            <h2 className="text-[15px] font-bold tracking-[-0.3px] sm:text-[16px]">
              Popular Categories
            </h2>

            <Link
              to="/menu"
              className="flex items-center gap-[2px] text-[8px] font-medium text-orange-500"
            >
              View All
              <ChevronRight size={11} />
            </Link>

          </div>


          <div className="grid grid-cols-5 gap-2 sm:gap-3">

            {data.categories.slice(0, 5).map((category) => (

              <Link
                key={category.id || category.name}
                to={`/menu?category=${encodeURIComponent(
                  category.name
                )}`}
                className="group relative h-[95px] overflow-hidden rounded-[6px] bg-gray-200 sm:h-[105px]"
              >

                <img
                  src={category.image}
                  alt={category.name}
                  className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
                />

                <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-black/10 to-transparent" />

                <span className="absolute bottom-2 left-2 text-[9px] font-bold text-white sm:text-[10px]">
                  {category.name}
                </span>

              </Link>

            ))}

          </div>

        </section>


        {/* =====================================================
            WEBSITE PAGE PREVIEW
        ===================================================== */}

        <section className="border-t border-gray-100 bg-gray-50 px-3 py-5 sm:px-8">

          <h2 className="mb-4 text-center text-[9px] font-bold tracking-wide text-gray-600">
            WEBSITE PAGES PREVIEW
          </h2>


          <div className="mx-auto grid max-w-[1100px] gap-3 md:grid-cols-3">


            {/* ================= MENU ================= */}

            <div className="overflow-hidden rounded-[5px] border border-gray-200 bg-white">

              <div className="flex h-[30px] items-center justify-center border-b border-gray-100 text-[7px] font-bold text-gray-500">
                MENU PAGE
              </div>

              <div className="p-3">

                <div className="grid grid-cols-[48px_1fr] gap-2">

                  {/* Sidebar */}

                  <div className="flex flex-col gap-3 text-[6px] text-gray-500">

                    <span className="font-bold text-orange-500">
                      All
                    </span>

                    <span>Pizza</span>
                    <span>Burgers</span>
                    <span>Chinese</span>
                    <span>Beverages</span>
                    <span>Desserts</span>

                  </div>


                  {/* Items */}

                  <div className="space-y-[7px]">

                    {data.menu.slice(0, 5).map((item) => (

                      <div
                        key={item.id || item.name}
                        className="grid grid-cols-[35px_1fr_auto] items-center gap-1.5"
                      >

                        <img
                          src={item.image}
                          alt={item.name}
                          className="h-[35px] w-[35px] rounded object-cover"
                        />

                        <div>

                          <p className="line-clamp-1 text-[7px] font-semibold">
                            {item.name}
                          </p>

                          <p className="text-[7px] font-medium text-orange-500">
                            ₹{item.price}
                          </p>

                        </div>

                        <button className="rounded-[3px] bg-orange-500 px-1.5 py-1 text-[5px] font-bold text-white">
                          ADD
                        </button>

                      </div>

                    ))}

                  </div>

                </div>

              </div>

            </div>


            {/* ================= TABLE BOOKING ================= */}

            <div className="overflow-hidden rounded-[5px] border border-gray-200 bg-white">

              <div className="flex h-[30px] items-center justify-center border-b border-gray-100 text-[7px] font-bold text-gray-500">
                TABLE BOOKING PAGE
              </div>

              <div className="p-3">

                <div className="space-y-1.5">

                  <h3 className="mb-2 flex items-center gap-1 text-[10px] font-bold">
                    <CalendarDays
                      size={11}
                      className="text-orange-500"
                    />
                    Book Your Table
                  </h3>


                  <PreviewInput
                    label="Restaurant"
                    value="SHP Restaurant, Civil Lines"
                  />

                  <PreviewInput
                    label="Date"
                    value="15 May 2025"
                  />

                  <PreviewInput
                    label="Time"
                    value="7:30 PM"
                  />

                  <PreviewInput
                    label="No. of Persons"
                    value="4 People"
                  />

                  <PreviewInput
                    label="Table Preference"
                    value="Any"
                  />


                  <Link
                    to="/booking"
                    className="mt-1 flex h-[24px] items-center justify-center rounded-[3px] bg-orange-500 text-[7px] font-semibold text-white"
                  >
                    Check Availability
                  </Link>


                  <img
                    src={data.restaurant.heroImage}
                    alt="Restaurant"
                    className="mt-1 h-[65px] w-full rounded-[3px] object-cover"
                  />

                </div>

              </div>

            </div>


            {/* ================= PARTY BOOKING ================= */}

            <div className="overflow-hidden rounded-[5px] border border-gray-200 bg-white">

              <div className="flex h-[30px] items-center justify-center border-b border-gray-100 text-[7px] font-bold text-gray-500">
                PARTY BOOKING PAGE
              </div>

              <div className="p-3">

                <div className="space-y-1.5">

                  <h3 className="mb-1 flex items-center gap-1 text-[10px] font-bold">
                    <UsersRound
                      size={11}
                      className="text-orange-500"
                    />
                    Plan Your Celebration
                  </h3>

                  <p className="mb-2 text-[7px] leading-[1.4] text-gray-500">
                    Make your special moments memorable
                    with us.
                  </p>


                  <PreviewInput
                    label="Occasion"
                    value="Birthday"
                  />

                  <PreviewInput
                    label="Date"
                    value="05 June 2025"
                  />

                  <PreviewInput
                    label="No. of Guests"
                    value="20 People"
                  />

                  <PreviewInput
                    label="Additional Requirements"
                    value="Decoration, Cake..."
                  />


                  <Link
                    to="/party-booking"
                    className="mt-2 flex h-[24px] items-center justify-center rounded-[3px] bg-orange-500 text-[7px] font-semibold text-white"
                  >
                    Send Request
                  </Link>

                </div>

              </div>

            </div>

          </div>

        </section>

      </main>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="flex min-h-[70px] items-center gap-5 border-t border-gray-100 px-5 sm:px-10">

        <Link
          to="/"
          className="text-[19px] font-black tracking-[-1.3px]"
        >
          {data.restaurant.name}
          <span className="text-orange-500">.</span>
        </Link>

        <p className="text-[8px] text-gray-500 sm:text-[9px]">
          Good food for great moments.
        </p>

      </footer>

    </div>
  );
}


/* ============================================================
   SMALL REUSABLE FORM COMPONENT
============================================================ */

function PreviewInput({ label=" ", value="" }) {
  return (
    <div>

      <label className="mb-1 block text-[6px] text-gray-500">
        {label}
      </label>

      <div className="flex h-[23px] items-center rounded-[3px] border border-gray-200 px-2 text-[7px] text-gray-600">
        {value}
      </div>

    </div>
  );
}
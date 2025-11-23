<template>
  <div
    class="w-screen h-screen font-['IBM_Plex_Sans'] overflow-y-scroll overflow-x-hidden snap-y snap-mandatory"
  >
    <!-- Section 1: Hero -->
    <section
      class="h-screen w-full flex flex-col justify-center items-start gap-3 px-6 md:gap-6 md:px-20 bg-gradient-to-b from-sky-50 via-blue-600/80 to-slate-900 snap-start relative"
    >
      <img
        src="/layer_2.png"
        alt="Decorative"
        style="z-index: 0;"
        class="hidden md:block fixed right-0 top-1/2 transform -translate-y-1/2 scale-70 pointer-events-none animate-slide-in-right w-1/2 object-cover object-left"
      />
      <div class="relative z-10 w-full max-w-4xl">
        <div
          class="flex flex-col justify-end items-start gap-3 animate-fade-in-up"
        >
          <b class="justify-start text-White text-3xl md:text-4xl font-bold">
            HireIT
          </b>
          <b class="justify-start text-White text-3xl md:text-6xl font-bold">
            Your AI Recruitment Orchestrator
          </b>
          <i
            class="justify-start text-White text-lg md:text-3xl font-bold italic"
          >
            One intelligent agent that coordinates your entire hiring workflow.
          </i>
        </div>
        <router-link
          to="/chat"
          class="px-6 py-4 bg-sky-50/20 rounded-2xl inline-flex justify-center items-center gap-2.5 hover:bg-sky-50/30 transition-colors w-fit animate-fade-in-up animation-delay-300"
        >
          <div
            class="justify-start text-white text-xl md:text-2xl font-bold font-['IBM_Plex_Sans']"
          >
            Get Started
          </div>
          <img
            class="w-10 h-10 relative max-h-full"
            alt="Arrow Icon"
            src="/mi_arrow-left.png"
          />
        </router-link>
      </div>
    </section>

    <!-- Section 2: Challenges -->
    <section
      class="h-screen w-full flex flex-col justify-center items-center px-6 md:px-20 bg-gradient-to-b from-slate-900 to-neutral-900 snap-start"
    >
      <div
        class="w-full max-w-7xl flex flex-col justify-center items-center gap-12"
      >
        <div
          class="self-stretch p-3 rounded-xl flex flex-col justify-end items-start gap-3"
        >
          <div
            class="self-stretch justify-start text-White text-2xl font-bold font-['IBM_Plex_Sans']"
          >
            The Challenges Behind Modern Recruitment
          </div>
        </div>
        <div
          class="self-stretch flex flex-col justify-start items-start gap-10"
        >
          <div
            class="self-stretch inline-flex justify-start items-start gap-10"
          >
            <div
              class="flex-1 self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex flex-col justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div
                class="self-stretch text-center justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                High Volume of CV
              </div>
              <div
                class="self-stretch text-center justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                HR spends too much time manually filtering large applicant
                pools.
              </div>
            </div>
            <div
              class="flex-1 self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex flex-col justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div
                class="self-stretch text-center justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                Fragmented Tools
              </div>
              <div
                class="self-stretch text-center justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                Recruitment happens across multiple apps that don’t talk to each
                other.
              </div>
            </div>
            <div
              class="flex-1 px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex flex-col justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div
                class="self-stretch text-center justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                Unstructured Interviews
              </div>
              <div
                class="self-stretch text-center justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                Evaluations vary widely between interviewers, reducing
                consistency.
              </div>
            </div>
          </div>
          <div
            class="self-stretch inline-flex justify-start items-center gap-10"
          >
            <div
              class="flex-1 px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex flex-col justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div
                class="self-stretch text-center justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                AI-Assisted Candidate Cheating
              </div>
              <div
                class="self-stretch text-center justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                New tools help candidates craft answers in real time, lowering
                interview integrity.
              </div>
            </div>
            <div
              class="flex-1 px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex flex-col justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div
                class="self-stretch text-center justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                Administrative Overload
              </div>
              <div
                class="self-stretch text-center justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                HR spends too much time manually filtering large applicant
                pools.
              </div>
            </div>
          </div>
        </div>
        <div
          class="self-stretch px-10 py-3 backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 shadow-lg inline-flex justify-center items-center gap-6"
        >
          <div class="text-center justify-start">
            <span class="text-White text-2xl font-bold font-['IBM_Plex_Sans']"
              >Result:</span
            ><span
              class="text-White text-2xl font-normal font-['IBM_Plex_Sans']"
            >
              slow hiring, inconsistent evaluation, and burnout.</span
            >
          </div>
        </div>
      </div>
    </section>

    <!-- Section 3: Solution -->
    <section
      class="h-screen w-full flex flex-col justify-center items-center px-6 md:px-20 bg-gradient-to-b from-neutral-900 to-slate-950 snap-start"
    >
      <div
        class="w-full max-w-7xl flex flex-col justify-center items-center gap-12"
      >
        <div
          class="self-stretch p-3 rounded-xl flex flex-col justify-end items-start gap-3"
        >
          <div
            class="self-stretch justify-start text-White text-4xl font-bold font-['IBM_Plex_Sans']"
          >
            Meet Our Solution
          </div>
          <div class="inline-flex justify-start items-center gap-3">
            <div
              class="justify-start text-White text-6xl font-bold font-['IBM_Plex_Sans']"
            >
              HireIT
            </div>
            <div
              class="w-12 h-0 outline outline-[5px] outline-offset-[-2.50px] outline-sky-50"
            ></div>
            <div
              class="justify-start text-White text-4xl font-medium font-['IBM_Plex_Sans']"
            >
              your recruitment autopilot
            </div>
          </div>
          <div
            class="self-stretch justify-start text-sky-50 text-xl font-normal font-['IBM_Plex_Sans'] leading-7 [text-shadow:_0px_4px_4px_rgb(0_0_0_/_0.25)]"
          >
            HireIT is a multi-agent AI platform that eliminates manual workload
            and reinforces structured, compliant decision-making across every
            stage of hiring.
          </div>
        </div>
        <div
          class="self-stretch flex flex-col justify-start items-start gap-10"
        >
          <div
            class="self-stretch inline-flex justify-start items-center gap-10"
          >
            <div
              class="flex-1 self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div class="w-20 h-20 relative overflow-hidden">
                <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/ic_round-auto-mode.png"
                />
              </div>
              <div
                class="flex-1 inline-flex flex-col justify-start items-start gap-3"
              >
                <div
                  class="self-stretch justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
                >
                  End-to-end automation
                </div>
                <div
                  class="self-stretch justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                >
                  AI executes operational tasks across the entire hiring
                  lifecycle.
                </div>
              </div>
            </div>
            <div
              class="flex-1 self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
            >
              <div class="w-20 h-20 relative overflow-hidden">
                <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/streamline-ultimate_human-resources-search-men.svg"
                />
              </div>
              <div
                class="flex-1 inline-flex flex-col justify-start items-start gap-3"
              >
                <div
                  class="self-stretch justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
                >
                  Human oversight preserved
                </div>
                <div
                  class="self-stretch justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                >
                  The system performs the work, but all final decisions stay
                  with HR.
                </div>
              </div>
            </div>
          </div>
          <div
            class="self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl inline-flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
          >
            <img class="w-72 h-12" src="/IBM_watsonx_logo.svg.png" />
            <div
              class="flex-1 inline-flex flex-col justify-start items-start gap-3"
            >
              <div
                class="self-stretch justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
              >
                Enterprise-ready orchestration
              </div>
              <div class="self-stretch justify-start">
                <span
                  class="text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                  >Powered by </span
                ><span
                  class="text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
                  >watsonx</span
                ><span
                  class="text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                >
                  Orchestrate for secure, scalable workflows.</span
                >
              </div>
            </div>
          </div>
        </div>
        <div
          class="self-stretch px-10 py-3 backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 shadow-lg inline-flex justify-center items-center gap-6"
        >
          <div
            class="justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
          >
            AI handles the work. Humans stay in control.
          </div>
        </div>
      </div>
    </section>

    <!-- Section 4: Why This Changes Everything -->
    <section
      class="h-screen w-full flex justify-start items-center px-6 md:px-20 bg-gradient-to-b from-slate-950 to-blue-950 snap-start gap-12"
    >
      <div
        class="w-72 p-3 rounded-xl flex flex-col justify-end items-start gap-3"
      >
        <div
          class="self-stretch justify-start text-White text-4xl font-medium font-['IBM_Plex_Sans']"
        >
          Why This Changes Everything
        </div>
      </div>
      <div
        class="flex-1 flex flex-col justify-start items-start gap-12 max-w-4xl"
      >
        <div
          class="self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
        >
          <div class="w-20 h-20 relative overflow-hidden flex-shrink-0">
            <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/hugeicons_ai-brain-03.svg"
                />
          </div>
          <div class="flex-1 flex flex-col justify-start items-start gap-6">
            <div
              class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
            >
              AI as the Central Orchestrator
            </div>
            <div
              class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
            >
              Functions as the system's "brain" and conductor, coordinating
              end-to-end workflows across real applications with precision and
              consistency.
            </div>
          </div>
        </div>
        <div
          class="self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
        >
          <div class="w-20 h-20 relative overflow-hidden flex-shrink-0">
            <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/streamline-ultimate_user-network.svg"
                />
          </div>
          <div class="flex-1 flex flex-col justify-start items-start gap-6">
            <div
              class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
            >
              Tangible, Real-World Impact
            </div>
            <div
              class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
            >
              HR teams save significant screening time, interviews become more
              objective, and anti-cheating mechanisms ensure verifiable
              integrity throughout the process.
            </div>
          </div>
        </div>
        <div
          class="self-stretch px-10 py-6 backdrop-blur-xl bg-white/5 rounded-3xl flex justify-start items-start gap-6 border border-white/10 shadow-lg hover:bg-white/10 transition-all"
        >
          <div class="w-20 h-20 relative overflow-hidden flex-shrink-0">
            <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/streamline-ultimate_human-resources-search-men.svg"
                />
          </div>
          <div class="flex-1 flex flex-col justify-start items-start gap-6">
            <div
              class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
            >
              The Future of Human–AI Collaboration
            </div>
            <div
              class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
            >
              AI absorbs the cognitive load of repetitive operations, while
              humans retain full authority over judgment, decisions, and
              governance.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 5: Core Capabilities -->
    <section
      class="w-full px-6 md:px-20 py-20 flex flex-col justify-center items-center gap-12 bg-gradient-to-b from-blue-950 to-slate-900 snap-start"
    >
      <div
        class="w-full max-w-7xl p-3 rounded-xl flex flex-col justify-end items-start gap-3"
      >
        <div
          class="self-stretch justify-start text-White text-4xl font-bold font-['IBM_Plex_Sans']"
        >
          Core Capabilities
        </div>
      </div>
      <div
        class="w-full max-w-7xl flex justify-start items-start gap-12 relative"
      >
        <!-- Left Column: Capability Titles -->
        <div class="w-80 flex flex-col justify-start items-start gap-12">
          <div
            class="px-3 rounded-xl flex flex-col justify-start items-start gap-3"
            style="min-height: 486px"
          >
            <div
              class="justify-start text-White text-3xl font-bold font-['IBM_Plex_Sans']"
            >
              Job Listing Creation
            </div>
            <div
              class="justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
            >
              Automated workspace setup with structured job listings and
              candidate tracking.
            </div>
          </div>
          <div
            class="px-3 rounded-xl flex flex-col justify-start items-start gap-3"
            style="min-height: 384px"
          >
            <div
              class="justify-start text-White text-3xl font-bold font-['IBM_Plex_Sans']"
            >
              Applicant Tracking Pipeline
            </div>
            <div
              class="justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
            >
              Your hiring pipeline, updated automatically in real-time.
            </div>
          </div>
          <div
            class="px-3 rounded-xl flex flex-col justify-start items-start gap-3"
          >
            <div
              class="justify-start text-White text-3xl font-bold font-['IBM_Plex_Sans']"
            >
              Interview Transcription
            </div>
            <div
              class="justify-start text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
            >
              Real-time transcription and structured interview documentation.
            </div>
          </div>
        </div>

        <!-- Center Column: Timeline with Numbers -->
        <div
          class="flex flex-col justify-start items-center"
          style="padding-top: 180px"
        >
          <div
            class="w-20 h-20 py-3 bg-sky-50 rounded-full flex justify-center items-center"
          >
            <div
              class="text-blue-600 text-4xl font-bold font-['IBM_Plex_Sans']"
            >
              01
            </div>
          </div>
          <div class="w-1 bg-sky-50" style="height: 380px"></div>
          <div
            class="w-20 h-20 py-3 bg-sky-50 rounded-full flex justify-center items-center"
          >
            <div
              class="text-blue-600 text-4xl font-bold font-['IBM_Plex_Sans']"
            >
              02
            </div>
          </div>
          <div class="w-1 bg-sky-50" style="height: 380px"></div>
          <div
            class="w-20 h-20 py-3 bg-sky-50 rounded-full flex justify-center items-center"
          >
            <div
              class="text-blue-600 text-4xl font-bold font-['IBM_Plex_Sans']"
            >
              03
            </div>
          </div>
        </div>

        <!-- Right Column: Details -->
        <div class="flex-1 flex flex-col justify-start items-start gap-12">
          <div
            class="self-stretch flex flex-col justify-start items-start gap-6"
          >
            <div
              class="self-stretch flex flex-col justify-start items-start gap-6"
            >
              <div
                class="self-stretch inline-flex justify-start items-center gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                  <div
                    class="w-11 h-11 left-[3.25px] top-[3.25px] absolute bg-White"
                  ></div>
                </div>
                <div
                  class="flex-1 justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                >
                  HR provides job requirements and position details
                </div>
              </div>
              <div
                class="self-stretch inline-flex justify-start items-start gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                  <div
                    class="w-11 h-11 left-[4.33px] top-[4.33px] absolute bg-White"
                  ></div>
                </div>
                <div
                  class="flex-1 inline-flex flex-col justify-start items-start gap-3"
                >
                  <div
                    class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                  >
                    Agent automatically:
                  </div>
                  <div
                    class="self-stretch flex flex-col justify-center items-start gap-2"
                  >
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Creates Google Drive folder structure
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Generates structured job listing JSON
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Sets up CV and Transcript subfolders
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Initializes applicant tracking spreadsheet
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="self-stretch px-10 py-3 backdrop-blur-xl bg-white/5 rounded-xl border border-white/10 shadow-lg inline-flex justify-center items-center gap-6"
            >
              <div class="flex-1 justify-start">
                <span
                  class="text-White text-xl font-bold font-['IBM_Plex_Sans'] leading-7"
                  >Output:</span
                ><span
                  class="text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                >
                  complete workspace ready for hiring process with downloadable
                  files.</span
                >
              </div>
            </div>
          </div>
          <div
            class="self-stretch h-96 flex flex-col justify-start items-start gap-6"
          >
            <div
              class="self-stretch flex flex-col justify-start items-start gap-6"
            >
              <div
                class="self-stretch inline-flex justify-start items-start gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                  <div
                    class="w-11 h-11 left-[4.33px] top-[4.33px] absolute bg-White"
                  ></div>
                </div>
                <div
                  class="flex-1 justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                >
                  Real-time Applicant Management
                </div>
              </div>
              <div
                class="self-stretch inline-flex justify-start items-start gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                  <div
                    class="w-11 h-11 left-[4.33px] top-[4.33px] absolute bg-White"
                  ></div>
                </div>
                <div
                  class="flex-1 inline-flex flex-col justify-start items-start gap-3"
                >
                  <div
                    class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                  >
                    Agent tracks:
                  </div>
                  <div
                    class="self-stretch flex flex-col justify-center items-start gap-2"
                  >
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Candidate information and contact details
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Application status through hiring stages
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Interview schedules and outcomes
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Updates spreadsheet automatically with progress
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="self-stretch px-10 py-3 backdrop-blur-xl bg-white/5 rounded-xl border border-white/10 shadow-lg inline-flex justify-center items-center gap-6"
            >
              <div
                class="flex-1 justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                This provides full visibility into hiring progress and candidate
                pipeline.
              </div>
            </div>
          </div>
          <div
            class="self-stretch flex flex-col justify-start items-start gap-6"
          >
            <div
              class="self-stretch flex flex-col justify-start items-start gap-6"
            >
              <div
                class="self-stretch inline-flex justify-start items-center gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                </div>
                <div
                  class="flex-1 justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                >
                  Interview Intelligence and Documentation
                </div>
              </div>
              <div
                class="self-stretch inline-flex justify-start items-start gap-6"
              >
                <div class="w-12 h-12 relative overflow-hidden">
                </div>
                <div
                  class="flex-1 inline-flex flex-col justify-start items-start gap-3"
                >
                  <div
                    class="self-stretch justify-center text-White text-2xl font-bold font-['IBM_Plex_Sans']"
                  >
                    During live or recorded interviews:
                  </div>
                  <div
                    class="self-stretch flex flex-col justify-center items-start gap-2"
                  >
                    <div
                      class="justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Transcribes conversation in real-time
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Captures interviewer questions and candidate responses
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Generates structured interview documentation
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Stores transcripts in organized folder structure
                    </div>
                    <div
                      class="self-stretch justify-center text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
                    >
                      Enables review and analysis of interview sessions
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="self-stretch px-10 py-3 backdrop-blur-xl bg-white/5 rounded-3xl border border-white/10 shadow-lg inline-flex justify-center items-center gap-6"
            >
              <div
                class="flex-1 justify-start text-White text-xl font-normal font-['IBM_Plex_Sans'] leading-7"
              >
                Interviewers maintain full control while AI handles
                documentation and organization.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 6: Multi-Agent Orchestration & CTA -->
    <section
      class="h-screen w-full px-6 md:px-20 py-20 flex flex-col justify-center items-center gap-12 bg-gradient-to-b from-slate-900 to-neutral-900 snap-start"
    >
      <div
        class="w-full max-w-7xl flex flex-col justify-center items-center gap-12"
      >
        <div
          class="w-full p-3 rounded-xl flex flex-col justify-end items-start gap-3"
        >
          <div
            class="self-stretch justify-start text-White text-4xl font-bold font-['IBM_Plex_Sans']"
          >
            Powered by coordinated multi-agent orchestration.
          </div>
          <div
            class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
          >
            HireIT operates through specialized AI agents—each responsible for a
            specific function:
          </div>
        </div>
        <div class="w-full flex flex-col justify-start items-start gap-6">
          <div class="w-full flex justify-start items-start gap-6">
            <div
              class="flex-1 p-3 bg-sky-50/20 rounded-xl flex flex-col justify-start items-start gap-3"
            >
              <div class="w-16 h-16 relative overflow-hidden">
                <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/union.svg"
                />
              </div>
              <div
                class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
              >
                Hiring Assistant
              </div>
            </div>
            <div
              class="flex-1 p-3 bg-sky-50/20 rounded-xl flex flex-col justify-start items-start gap-3"
            >
              <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/union.svg"
                />
              <div
                class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
              >
                Interview Agent
              </div>
            </div>
            <div
              class="flex-1 p-3 bg-sky-50/20 rounded-xl flex flex-col justify-start items-start gap-3"
            >
              <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/union.svg"
                />
              <div
                class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
              >
                CV Reviewer Agent
              </div>
            </div>
            <div
              class="flex-1 p-3 bg-sky-50/20 rounded-xl flex flex-col justify-start items-start gap-3"
            >
              <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/union.svg"
                />
              <div
                class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
              >
                Job Listing Agent
              </div>
            </div>
            <div
              class="flex-1 p-3 bg-sky-50/20 rounded-xl flex flex-col justify-start items-start gap-3"
            >
              <img
                  class="relative max-h-full"
                  alt="Arrow Icon"
                  src="/union.svg"
                />
              <div
                class="self-stretch justify-start text-White text-2xl font-normal font-['IBM_Plex_Sans']"
              >
                Applicant Agent
              </div>
            </div>
          </div>
        </div>
        <div
          class="w-full px-20 py-12 bg-gradient-to-b from-sky-50 to-blue-600/70 rounded-3xl flex flex-col justify-center items-center gap-6"
        >
          <div
            class="w-full p-3 rounded-xl flex flex-col justify-center items-center gap-3"
          >
            <div
              class="self-stretch text-center justify-start text-blue-600 text-4xl font-bold font-['IBM_Plex_Sans']"
            >
              Transform your hiring operations.
            </div>
            <div
              class="self-stretch text-center justify-start text-blue-600 text-2xl font-normal font-['IBM_Plex_Sans']"
            >
              Bring efficiency, clarity, and control to every step of
              recruitment.
            </div>
            <router-link
              to="/chat"
              class="px-10 py-6 bg-blue-600/80 rounded-3xl flex justify-center items-center gap-2.5 hover:bg-blue-600 transition-all"
            >
              <div
                class="justify-start text-sky-50 text-xl font-bold font-['IBM_Plex_Sans'] uppercase leading-7"
              >
                Get Started
              </div>
              <img
                class="w-10 h-10 relative max-h-full"
                alt="Arrow Icon"
                src="/mi_arrow-left.png"
              />
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup></script>

<style>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,700;0,800;1,400;1,700;1,800&display=swap");
</style>

<style scoped>
/* Animation keyframes */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 0.8;
    transform: translateX(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-in-right {
  animation: slideInRight 1.2s ease-out forwards;
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}

.font-ibm-plex-sans {
  font-family: "IBM Plex Sans", sans-serif;
}
</style>

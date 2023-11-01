import OnboardingLayout from "@/layouts/OnboardingLayout";
import RootLayout from "@/layouts/RootLayout";

export default function Home() {
  return (
    <RootLayout>
      <OnboardingLayout>
        <div className="w-full flex flex-row px-20">
          <h1>Welcome Home</h1>
        </div>
      </OnboardingLayout>
    </RootLayout>
  );
}

//
//  ContentView.swift
//  swiftyapp
//
//  Created by Jonathan McKenzie on 7/9/24.
//

import RustyLib
import SwiftUI

struct ContentView: View {
    @State private var firstValue = 10
    @State private var secondValue = 32

    private var sum: Int {
        Int(rustAdd(a: UInt32(firstValue), b: UInt32(secondValue)))
    }

    var body: some View {
        ZStack {
            LinearGradient(
                colors: [
                    Color(red: 0.09, green: 0.11, blue: 0.20),
                    Color(red: 0.14, green: 0.18, blue: 0.31),
                    Color(red: 0.21, green: 0.15, blue: 0.34)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    header

                    glassCard {
                        VStack(alignment: .leading, spacing: 12) {
                            Label("Rust bridge", systemImage: "bolt.horizontal.circle.fill")
                                .font(.headline)
                                .foregroundStyle(.white.opacity(0.95))

                            Text(rustHello())
                                .font(.title2.weight(.semibold))
                                .foregroundStyle(.white)

                            Text("This SwiftUI app is wired directly into a Rust library through UniFFI.")
                                .font(.subheadline)
                                .foregroundStyle(.white.opacity(0.72))
                        }
                    }

                    glassCard {
                        VStack(alignment: .leading, spacing: 16) {
                            HStack {
                                Label("Live calculator", systemImage: "function")
                                    .font(.headline)
                                    .foregroundStyle(.white.opacity(0.95))
                                Spacer()
                                Text("Rust powered")
                                    .font(.caption.weight(.semibold))
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(.white.opacity(0.12), in: Capsule())
                                    .foregroundStyle(.white.opacity(0.9))
                            }

                            stepperRow(
                                title: "First value",
                                value: $firstValue,
                                range: 0...100
                            )

                            stepperRow(
                                title: "Second value",
                                value: $secondValue,
                                range: 0...100
                            )

                            Divider()
                                .overlay(.white.opacity(0.15))

                            HStack(alignment: .firstTextBaseline) {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text("Result")
                                        .font(.caption.weight(.semibold))
                                        .foregroundStyle(.white.opacity(0.7))
                                    Text("\(firstValue) + \(secondValue)")
                                        .font(.title3.weight(.semibold))
                                        .foregroundStyle(.white)
                                }

                                Spacer()

                                Text("\(sum)")
                                    .font(.system(size: 42, weight: .bold, design: .rounded))
                                    .foregroundStyle(
                                        LinearGradient(
                                            colors: [.white, Color(red: 0.76, green: 0.88, blue: 1.0)],
                                            startPoint: .top,
                                            endPoint: .bottom
                                        )
                                    )
                            }

                            Button {
                                firstValue = Int.random(in: 0...100)
                                secondValue = Int.random(in: 0...100)
                            } label: {
                                Label("Randomize values", systemImage: "dice.fill")
                                    .frame(maxWidth: .infinity)
                            }
                            .buttonStyle(PrimaryButtonStyle())
                        }
                    }

                    glassCard {
                        VStack(alignment: .leading, spacing: 10) {
                            Label("What this proves", systemImage: "checkmark.seal.fill")
                                .font(.headline)
                                .foregroundStyle(.white.opacity(0.95))

                            ForEach([
                                "SwiftUI rendering",
                                "State-driven interactions",
                                "Native Rust function calls",
                            ], id: \.self) { item in
                                HStack(spacing: 10) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .foregroundStyle(.green.opacity(0.9))
                                    Text(item)
                                        .foregroundStyle(.white.opacity(0.88))
                                    Spacer()
                                }
                                .font(.subheadline)
                            }
                        }
                    }
                }
                .padding(20)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Swifty Rust")
                        .font(.system(size: 34, weight: .bold, design: .rounded))
                        .foregroundStyle(.white)

                    Text("A polished SwiftUI shell around your Rust core.")
                        .font(.subheadline)
                        .foregroundStyle(.white.opacity(0.72))
                }

                Spacer()

                Image(systemName: "swift")
                    .font(.system(size: 28, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.95))
                    .padding(14)
                    .background(.white.opacity(0.12), in: RoundedRectangle(cornerRadius: 18, style: .continuous))
            }

            HStack(spacing: 8) {
                pill(text: "SwiftUI")
                pill(text: "UniFFI")
                pill(text: "Rust")
            }
        }
        .padding(.bottom, 4)
    }

    private func pill(text: String) -> some View {
        Text(text)
            .font(.caption.weight(.semibold))
            .padding(.horizontal, 12)
            .padding(.vertical, 7)
            .background(.white.opacity(0.12), in: Capsule())
            .foregroundStyle(.white.opacity(0.9))
    }

    private func glassCard<Content: View>(@ViewBuilder content: () -> Content) -> some View {
        content()
            .padding(18)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.white.opacity(0.12), in: RoundedRectangle(cornerRadius: 24, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .stroke(.white.opacity(0.14), lineWidth: 1)
            )
            .shadow(color: .black.opacity(0.18), radius: 18, x: 0, y: 10)
    }

    private func stepperRow(title: String, value: Binding<Int>, range: ClosedRange<Int>) -> some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                    .foregroundStyle(.white.opacity(0.92))
                Text("Tap +/- or use the randomizer")
                    .font(.caption)
                    .foregroundStyle(.white.opacity(0.62))
            }

            Spacer()

            Stepper(value: value, in: range) {
                Text("\(value.wrappedValue)")
                    .font(.title3.weight(.semibold))
                    .monospacedDigit()
                    .foregroundStyle(.white)
                    .frame(minWidth: 44, alignment: .trailing)
            }
            .labelsHidden()
            .tint(.white)
        }
    }
}

private struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline.weight(.semibold))
            .padding(.vertical, 14)
            .foregroundStyle(.white)
            .background(
                LinearGradient(
                    colors: [
                        Color(red: 0.33, green: 0.60, blue: 1.0),
                        Color(red: 0.67, green: 0.39, blue: 1.0)
                    ],
                    startPoint: .leading,
                    endPoint: .trailing
                ),
                in: RoundedRectangle(cornerRadius: 16, style: .continuous)
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(configuration.isPressed ? 0.92 : 1.0)
    }
}

#Preview {
    ContentView()
}

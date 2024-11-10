import requests
import dns.resolver
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button

# Function to perform a DNS over HTTPS (DoH) query
def doh_query(domain):
    doh_url = "https://cloudflare-dns.com/dns-query"
    headers = {"accept": "application/dns-json"}
    params = {"name": domain, "type": "A"}

    try:
        response = requests.get(doh_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        
        # Extract IP addresses if available
        if 'Answer' in result:
            return [answer['data'] for answer in result['Answer']]
        else:
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("DoH Query Error", f"Error querying DoH: {e}")
        return None

# Function to perform a DNS query using the system's default resolver
def system_dns_query(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return [answer.to_text() for answer in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return None
    except dns.exception.DNSException as e:
        messagebox.showerror("System DNS Error", f"System DNS query error: {e}")
        return None

# Function to detect DNS spoofing by comparing DoH and system DNS results
def detect_dns_spoofing():
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showwarning("Input Error", "Please enter a domain name.")
        return

    # Perform both DoH and system DNS queries
    doh_ips = doh_query(domain)
    system_ips = system_dns_query(domain)

    # Check for DNS spoofing by comparing IP lists
    if doh_ips and system_ips:
        if set(doh_ips) == set(system_ips):
            result_text.set(f"Domain: {domain}\nIP Addresses match.\nNo DNS spoofing detected.")
        else:
            result_text.set(f"WARNING: Possible DNS Spoofing Detected!\n\nDomain: {domain}\n"
                            f"DoH IPs: {', '.join(doh_ips)}\nSystem DNS IPs: {', '.join(system_ips)}")
    else:
        result_text.set("Error: Unable to retrieve DNS records. Check domain and network settings.")

# GUI setup using tkinter
app = tk.Tk()
app.title("DNS Spoofing Detection Tool")
app.geometry("450x300")

# Input label and entry field
Label(app, text="Enter Domain Name:", font=("Arial", 12)).pack(pady=10)
domain_entry = Entry(app, width=35, font=("Arial", 12))
domain_entry.pack(pady=5)

# Button to check for DNS spoofing
lookup_button = Button(app, text="Check for DNS Spoofing", command=detect_dns_spoofing, font=("Arial", 12), bg="lightblue")
lookup_button.pack(pady=15)

# Result display label
result_text = tk.StringVar()
result_label = Label(app, textvariable=result_text, font=("Arial", 10), justify="left", wraplength=400)
result_label.pack(pady=10)

# Run the application
app.mainloop()
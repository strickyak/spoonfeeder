# On the idea of emulating the Wiznet 5100S indirect interface

strick :: Tue Apr 23 2024

## Four Ports for the indirect interface.

The "indirect" interface has four 8-bit ports, which is
what the CocoIOr uses.
(The other two interfaces are "direct" where an address
subspace of 32K is used, and SPI.)
On the CocoIOr board, the four ports map to either $FF6[8-B] or $FF7[8-B]
in the 6809's address space.

FrobIO only uses a small subset of the capabilities,
so that is all we need to support.  So some of the
following statements may not be generally true,
but they are true of the subset we need.

## An Aardvark-like suggestion

Consider the four ports to be three control ports and one data port:

```
[control]  Reset/Mode/Status (usually write-only, but reads $03 when probing)

[control]  Hi Byte of [wiznet register] Addr (usually write-only)

[control]  Lo Byte of [wiznet register] Addr (usually write-only)

[data]     Data Read or Write
```

In the Aardvark sense, use two state machines:
one for the three control ports, and one for
data.   The data machine is ready to look at R/W
to decide whether to read or write.  Once it
decides R or W, it will not change R or W
until there are more writes to the Addr bytes.

Writing the Hi Byte of the Addr just stores it.

Writing the Lo Byte of the Addr sets up two DMAs,
one for reading and one for writing.
Only one of these two will actually be used,
but we don't know which until the first Read or
Write on the data port happens.
It also sets up the second State Machine to
operate the Data port.

The first state machine is still looking for
writes to the Control Ports, which will stop
the second state machine until we know what
that machine will do next.

Simiar to the Aardvark, hardware could decode the
$FF6[8-B] address range.  This Chip Select
plus A0 and A1 and R/W and E could drive the
state machines.

## Wiznet Register Summary

The wiznet contains 16K of general-purpose packet buffer
RAM, 8K for transmit and 8K for receive.  So far we
use the default configuration where each of the four
sockets gets 2K transmit and 2K receive buffer
for itself.

Then there are other registers, of several sorts:

*   Configuration you write: MAC addr, IP addr,
	IP gateway, timeout values, options.

*   Pointers you write, for the circular buffers
	used in Transmit and Receive.

*   Pointers and length values you read,
	for those buffers.

*   A mode register, for UDP vs TCP vs Closed.

*   A command register, for Open and Send and
	Receive and Close.   Reading this register
	returns non-zero while the command is
	still processing, and zero when it is done.

*   An interrupt register, where bits appear
	for conditions like Sent and Received
	and Timeout and Connection Closed.

*   Other things like a free-running counter
	with 0.1 millisecond granularity.

From the Address that was written
to the Hi and Lo addr control ports,
we know which of these types it will be.
New Hi and Lo addrs will be written before
the nature of the data changes.


## Mininum Product: one TCP client

For most usage with the Lemma server, a single TCP
client on the Wiznet is enough.

(The Axiom BOOTROM also uses UDP (broadcast) for
DHCP and LAN Lemma discovery, but the CoPiCo
doesn't have to follow that path.  Config could
be provided externally over the USB and held
in the CoPiCo, for instance.)

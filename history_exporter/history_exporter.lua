local addonName, addon = ...

-- SavedVariables table
MyAddon_auctionHistory = MyAddon_auctionHistory or { scans = {}, export = {} }

local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_LOGOUT")

-- scanning state
local currentScan = nil
local collected = 0

local function saveCurrentScan()
    if currentScan and #currentScan.data > 0 then
        table.insert(MyAddon_auctionHistory.scans, currentScan)
    end
    currentScan = nil
end

local function processAuctions()
    local numBatch, total = GetNumAuctionItems("list")
    for i = collected + 1, numBatch do
        local name, texture, count, quality, usable, level, startPrice, minIncrement, buyoutPrice, highBid, highBidder, owner = GetAuctionItemInfo("list", i)
        local timeLeft = GetAuctionItemTimeLeft("list", i)
        local link = GetAuctionItemLink("list", i)
        local itemId = link and tonumber(string.match(link, "item:(%d+)") or 0) or 0

        table.insert(currentScan.data, {
            itemID = itemId,
            count = count,
            buyout = buyoutPrice,
            bid = startPrice,
            owner = owner,
            highBidder = highBidder,
            timeLeft = timeLeft,
        })
    end
    collected = numBatch
    if numBatch == total then
        frame:UnregisterEvent("AUCTION_ITEM_LIST_UPDATE")
        saveCurrentScan()
    end
end

local function beginFullScan()
    if currentScan or not CanSendAuctionQuery() then return end
    currentScan = { time = time(), data = {} }
    collected = 0
    frame:RegisterEvent("AUCTION_ITEM_LIST_UPDATE")
    QueryAuctionItems("", nil, nil, 0, 0, 0, 0, 0, true)
end

-- Expose slash command to trigger scanning
SLASH_AUXHISTORYEXPORTER1 = "/auxscan"
SlashCmdList["AUXHISTORYEXPORTER"] = beginFullScan

frame:SetScript("OnEvent", function(self, event, ...)
    if event == "AUCTION_ITEM_LIST_UPDATE" then
        processAuctions()
    elseif event == "PLAYER_LOGOUT" then
        -- also export Aux's internal auction database
        MyAddon_auctionHistory.export = aux and aux.faction_data and aux.faction_data.auctions or {}
        saveCurrentScan()
    end
end)

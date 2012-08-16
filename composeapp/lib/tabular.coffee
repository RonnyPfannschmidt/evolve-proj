class TableWriter
  constructor: (@send_one, @items, @discriminate) ->
    @buffers = new Array(@items.length)
    for i in [1..@items.length]
      @buffers[i] = new Array()

  make_header: (maker) ->
    @header_maker = maker
    maker @send_one, @items[0]

  make_rows: (getRow, maker) ->
    while row = getRow()
      maker @send_one, row

  finalize: () ->
    for buffer in @buffers
      buffer.forEach @send_one

exports.TableWriter = TableWriter

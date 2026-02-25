import React from 'react'
import { Checkbox, ListItemText, Menu, MenuItem } from '@mui/material'

interface Option {
  label: string
  value: string
}

interface FilterMenuProps {
  button: (props: {
    'onClick': (event: React.MouseEvent<HTMLElement>) => void
    'aria-controls'?: string
    'aria-haspopup'?: 'true'
    'aria-expanded'?: 'true' | 'false'
  }) => React.ReactElement
  options: Option[]
  value: string | string[]
  onChange: (val: any) => void
  multiple?: boolean
  disabled?: boolean
}

export const FilterMenu: React.FC<FilterMenuProps> = ({
  button,
  options,
  value,
  onChange,
  multiple = false,
  disabled = false,
}) => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)

  const handleOpen = (event: React.MouseEvent<HTMLElement>) => {
    if (!disabled) {
      setAnchorEl(event.currentTarget)
    }
  }
  const handleClose = () => setAnchorEl(null)

  const handleSelect = (selectedValue: string) => {
    if (multiple) {
      const newValue = Array.isArray(value)
        ? value.includes(selectedValue)
          ? value.filter(v => v !== selectedValue)
          : [...value, selectedValue]
        : [selectedValue]
      onChange(newValue)
    }
    else {
      onChange(selectedValue)
      handleClose()
    }
  }

  const menuId = 'filter-menu'

  return (
    <>
      {button({
        'onClick': handleOpen,
        'aria-controls': open ? menuId : undefined,
        'aria-haspopup': 'true',
        'aria-expanded': open ? 'true' : 'false',
      })}
      <Menu
        id={menuId}
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        {options.map(opt => (
          <MenuItem key={opt.value} onClick={() => handleSelect(opt.value)}>
            {multiple && (
              <Checkbox
                sx={{ 'color': 'brown', '&.Mui-checked': { color: 'brown' } }}
                checked={Array.isArray(value) && value.includes(opt.value)}
              />
            )}
            <ListItemText primary={opt.label} />
          </MenuItem>
        ))}
      </Menu>
    </>
  )
}
